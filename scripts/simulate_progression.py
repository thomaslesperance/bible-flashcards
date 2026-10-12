"""
Prototype: generate the A/F/B/C/D + seam + keyword card progression for the
Sermon on the Mount, write it as an Anki .apkg (Basic notes, deck order =
intended new-card order), and simulate day-by-day reviews to CSV.

Throwaway exploration code -- not the real compiler.

Usage: python scripts/simulate_progression.py [--new-per-day 12] [--days 90]
"""
import argparse
import csv
import html
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
BSB_PATH = BASE_DIR / "data" / "raw" / "bsb.csv"
OUTLINE_PATH = BASE_DIR / "data" / "outlines" / "sermon_on_the_mount.yml"
OUT_DIR = BASE_DIR / "output" / "som_preview"

TARGET_V, MAX_V, MIN_V, MERGE_MAX = 4, 5, 3, 6
BIG_NODE = 20  # nodes larger than this use headers/keywords instead of full text

# --------------------------------------------------------------------------
# Text + outline
# --------------------------------------------------------------------------

def load_matthew():
    verses = []
    with open(BSB_PATH, encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[1].startswith("Matthew "):
                ch, v = row[1].split(" ")[1].split(":")
                verses.append((int(ch), int(v), row[2].strip()))
    index = {(c, v): i for i, (c, v, _) in enumerate(verses)}
    return verses, index


def ref_range(ref, index):
    a, b = ref.split("-")
    ca, va = map(int, a.split(":"))
    cb, vb = map(int, b.split(":"))
    return list(range(index[(ca, va)], index[(cb, vb)] + 1))


@dataclass
class Node:
    title: str
    verses: list
    parent: "Node" = None
    children: list = field(default_factory=list)
    paragraphs: list = None
    depth: int = 0

    @property
    def is_leaf(self):
        return not self.children


def build_tree(spec, title, index, parent=None, depth=0):
    node = Node(title, ref_range(spec["ref"], index), parent, depth=depth)
    if spec.get("paragraphs"):
        node.paragraphs = [ref_range(p, index) for p in spec["paragraphs"]]
    for t, s in (spec.get("sections") or {}).items():
        node.children.append(build_tree(s, t, index, node, depth + 1))
    return node


def leaves(node):
    if node.is_leaf:
        yield node
    for c in node.children:
        yield from leaves(c)


def walk(node):
    yield node
    for c in node.children:
        yield from walk(c)

# --------------------------------------------------------------------------
# Study units
# --------------------------------------------------------------------------

@dataclass
class Unit:
    verses: list
    segments: list  # [(leaf, verse_idxs, part_label)]
    idx: int = 0


def partition(blocks):
    """Split a list of verse blocks into contiguous chunks <= MAX_V verses,
    minimising squared distance from TARGET_V. Blocks are never broken."""
    n = len(blocks)
    best = {n: (0, [])}
    for i in range(n - 1, -1, -1):
        options = []
        size = 0
        for j in range(i, n):
            size += len(blocks[j])
            if size > MAX_V and j > i:
                break
            cost, rest = best[j + 1]
            options.append((cost + (size - TARGET_V) ** 2, [(i, j + 1)] + rest))
        best[i] = min(options, key=lambda o: o[0])
    return [sum(blocks[a:b], []) for a, b in best[0][1]]


def build_units(root):
    units = []
    for leaf in leaves(root):
        blocks = leaf.paragraphs or [[v] for v in leaf.verses]
        chunks = partition(blocks) if len(leaf.verses) > MAX_V else [leaf.verses]
        for k, ch in enumerate(chunks):
            label = f" (part {k + 1} of {len(chunks)})" if len(chunks) > 1 else ""
            units.append(Unit(ch, [(leaf, ch, label)]))

    def parent_of(u):
        return u.segments[0][0].parent

    merged = True
    while merged:
        merged = False
        for i, u in enumerate(units):
            if len(u.verses) >= MIN_V:
                continue
            for j in (i + 1, i - 1):  # prefer merging forward
                if 0 <= j < len(units) and parent_of(units[j]) is parent_of(u) \
                        and len(units[j].verses) + len(u.verses) <= MERGE_MAX:
                    a, b = sorted((i, j))
                    units[a] = Unit(units[a].verses + units[b].verses,
                                    units[a].segments + units[b].segments)
                    del units[b]
                    merged = True
                    break
            if merged:
                break
    for i, u in enumerate(units):
        u.idx = i
    return units

# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

STOP = set("""that this with have will your they them their theirs those these
from into what when then there were been also does shall unto which would
should could because whoever anyone everyone said says tell truly than about
over upon very even more much just like only being every some other such
whom whose here where while until after before again against through""".split())


def words(text):
    return re.findall(r"[A-Za-z’']+", text)


def make_keywords(verses, root):
    df = Counter()
    for i in root.verses:
        df.update({w.lower() for w in words(verses[i][2])})
    kw = {}
    for i in root.verses:
        recent = {kw.get(j) for j in range(i - 4, i)}
        cands = [w.lower().strip("’'") for w in words(verses[i][2])]
        cands = [w for w in cands if len(w) >= 4 and w not in STOP and w not in recent] or ["—"]
        pick = next((w for w in cands if df[w] <= 2), None)
        kw[i] = pick or (min(cands, key=lambda w: df[w]) if cands else "—")
    return kw


def initials(text):
    out = []
    for tok in text.split():
        m = re.match(r"^([^A-Za-z0-9]*)([A-Za-z0-9])[A-Za-z0-9’'\-]*([^A-Za-z0-9]*)$", tok)
        out.append(m.group(1) + m.group(2) + m.group(3) if m else tok)
    return " ".join(out)


# --------------------------------------------------------------------------
# Cards
# --------------------------------------------------------------------------

@dataclass
class Card:
    step: str
    kind: str
    unit: int
    node: str
    ref: str
    front: list  # list of (text, hidden?) lines; html built later
    back: list
    pos: int = 0


class Builder:
    def __init__(self, verses, root, units):
        self.v, self.root, self.units = verses, root, units
        self.kw = make_keywords(verses, root)
        self.cards = []

    # ---- formatting
    def ref(self, idxs):
        (c1, v1, _), (c2, v2, _) = self.v[idxs[0]], self.v[idxs[-1]]
        if idxs[0] == idxs[-1]:
            return f"Matt {c1}:{v1}"
        return f"Matt {c1}:{v1}–{v2}" if c1 == c2 else f"Matt {c1}:{v1}–{c2}:{v2}"

    def vt(self, i):
        c, v, t = self.v[i]
        return f"{v} {t}"

    def kwchain(self, idxs):
        return " · ".join(self.kw[i] for i in idxs)

    def path(self, node):
        parts = []
        while node is not None and node is not self.root:
            parts.append(node.title)
            node = node.parent
        return " › ".join(reversed(parts)) or self.root.title

    def add(self, step, kind, unit, node, idxs, front, back):
        self.cards.append(Card(step, kind, unit, node, self.ref(idxs), front, back))

    # ---- card families
    def preview(self, node, u):
        titles = [c.title for c in node.children]
        for k in range(len(titles)):
            front = [(f"Outline of “{node.title}”", "ctx")] + [
                ("[...]" if j == k else f"{j + 1}. {t}", "hide" if j == k else "")
                for j, t in enumerate(titles)]
            back = [(f"Outline of “{node.title}”", "ctx")] + [
                (f"{j + 1}. {t}", "ans" if j == k else "") for j, t in enumerate(titles)]
            self.add("P", "outline preview (one header hidden)", u, node.title,
                     node.verses, front, back)

    def step_a(self, u, prev):
        ctx = (f"{' / '.join(s[0].title + s[2] for s in u.segments)} · {self.ref(u.verses)}", "ctx")
        for i in u.verses:
            front = [ctx] + [("[...]" if j == i else self.vt(j), "hide" if j == i else "")
                             for j in u.verses]
            back = [ctx] + [(self.vt(j), "ans" if j == i else "") for j in u.verses]
            self.add("A", "scaffolded cloze (one verse hidden)", u.idx,
                     self.path(u.segments[0][0]), [i], front, back)
        if prev is not None:
            a, b = prev.verses[-1], u.verses[0]
            ctx2 = (f"Seam · {self.ref([a])} → {self.ref([b])}", "ctx")
            self.add("A", "seam (next verse across units)", u.idx,
                     self.path(u.segments[0][0]), [a, b],
                     [ctx2, (self.vt(a), ""), ("[...]", "hide")],
                     [ctx2, (self.vt(a), ""), (self.vt(b), "ans")])
        for leaf, idxs, label in u.segments:
            body = [(self.vt(j), "") for j in idxs]
            self.add("A", "text → header", u.idx, self.path(leaf), idxs,
                     [("Which section is this?", "ctx")] + body,
                     [("Which section is this?", "ctx"),
                      (f"{self.path(leaf)}{label}", "ans")] + body)

    def step_f(self, u):
        ctx = (f"First letters · {' / '.join(s[0].title + s[2] for s in u.segments)} · {self.ref(u.verses)}", "ctx")
        self.add("F", "first letters → text", u.idx, self.path(u.segments[0][0]), u.verses,
                 [ctx] + [(f"{self.v[j][1]} {initials(self.v[j][2])}", "") for j in u.verses],
                 [ctx] + [(self.vt(j), "ans") for j in u.verses])

    def step_b(self, u):
        if len(u.verses) > 3:
            ctx = (f"Anchored · {self.ref(u.verses)}", "ctx")
            mid = u.verses[1:-1]
            self.add("B", "anchored recall (middle hidden)", u.idx,
                     self.path(u.segments[0][0]), u.verses,
                     [ctx, (self.vt(u.verses[0]), ""), (f"[... {len(mid)} verses ...]", "hide"),
                      (self.vt(u.verses[-1]), "")],
                     [ctx] + [(self.vt(j), "ans" if j in mid else "") for j in u.verses])
        for leaf, idxs, label in u.segments:
            head = (f"{self.path(leaf)}{label}", "ctx")
            self.add("B", "header → keywords", u.idx, self.path(leaf), idxs,
                     [head, ("Keywords, one per verse?", "hide")],
                     [head, (self.kwchain(idxs), "ans")])
            self.add("B", "header → text", u.idx, self.path(leaf), idxs,
                     [head, (f"Recite {self.ref(idxs)}", "hide")],
                     [head] + [(self.vt(j), "ans") for j in idxs])

    def unit_blocks(self, node):
        """Child blocks of a node: real children, or chunks of a split leaf."""
        if node.children:
            return [(c.title, c.verses) for c in node.children]
        return [(f"part {k + 1}", u.verses) for k, u in enumerate(
            u for u in self.units if u.segments[0][0] is node)]

    def step_c(self, node, u):
        blocks = self.unit_blocks(node)
        head = (self.path(node), "ctx")
        if node.children:
            titles = [c.title for c in node.children]
            self.add("C", "header → full outline", u, self.path(node), node.verses,
                     [head, (f"List its {len(titles)} sections in order", "hide")],
                     [head] + [(f"{j + 1}. {t}", "ans") for j, t in enumerate(titles)])
        if len(node.verses) <= BIG_NODE:
            for k, (title, idxs) in enumerate(blocks):
                front, back = [head], [head]
                for j, (t2, ix2) in enumerate(blocks):
                    if j == k:
                        front.append((f"[... {t2}: {self.ref(ix2)} ...]", "hide"))
                        back += [(self.vt(i), "ans") for i in ix2]
                    else:
                        front += [(self.vt(i), "") for i in ix2]
                        back += [(self.vt(i), "") for i in ix2]
                self.add("C", "missing sub-section text", u, self.path(node), idxs, front, back)
            self.add("C", "first letters → text (whole section)", u, self.path(node), node.verses,
                     [head] + [(f"{self.v[j][1]} {initials(self.v[j][2])}", "") for j in node.verses],
                     [head] + [(self.vt(j), "ans") for j in node.verses])

    def step_d(self, node, u):
        head = (self.path(node), "ctx")
        if len(node.verses) <= BIG_NODE:
            self.add("D", "header → full text (whole section)", u, self.path(node), node.verses,
                     [head, (f"Recite {self.ref(node.verses)}", "hide")],
                     [head] + [(self.vt(j), "ans") for j in node.verses])
        elif node.children and len(node.verses) <= 40:
            self.add("D", "header → sections + keyword chains", u, self.path(node), node.verses,
                     [head, ("Each section with its keywords", "hide")],
                     [head] + [(f"{c.title}: {self.kwchain(c.verses)}", "ans") for c in node.children])

    # ---- sequencing
    def build(self):
        units = self.units
        first_unit = {}
        last_unit = {}
        for u in units:
            for v in u.verses:
                for n in walk(self.root):
                    if v in n.verses:
                        first_unit.setdefault(id(n), u.idx)
                        last_unit[id(n)] = u.idx
        nodes = list(walk(self.root))
        sched = defaultdict(list)

        def run(k):
            for fn in sched.pop(k, []):
                fn()

        for u in units:
            k = u.idx
            for n in nodes:  # top-down previews for sections starting here
                if first_unit[id(n)] == k and len(n.children) >= 2:
                    self.preview(n, k)
            self.step_a(u, units[k - 1] if k else None)
            run(k)
            sched[k + 1].append(lambda u=u: self.step_f(u))
            sched[k + 2].append(lambda u=u: self.step_b(u))
            closing = [n for n in nodes if last_unit[id(n)] == k
                       and first_unit[id(n)] != k and n.verses != u.verses]
            closing.sort(key=lambda n: -n.depth)  # innermost first
            for off, n in enumerate(closing):
                sched[k + 3 + off].append(lambda n=n, k=k: self.step_c(n, k))
                sched[k + 4 + off].append(lambda n=n, k=k: self.step_d(n, k))
        k = len(units)
        while sched:
            run(k)
            k += 1
        for p, c in enumerate(self.cards, 1):
            c.pos = p
        return self.cards

# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def to_html(lines):
    out = []
    for text, style in lines:
        t = html.escape(text)
        out.append({"ctx": f'<div class="ctx">{t}</div>',
                    "hide": f'<div class="hide">{t}</div>',
                    "ans": f'<div class="ans">{t}</div>'}.get(style, f"<div>{t}</div>"))
    return "\n".join(out)


def to_plain(lines):
    return " | ".join(t for t, _ in lines)


CSS = """
.card { font-family: Georgia, serif; font-size: 20px; line-height: 1.5;
        text-align: left; max-width: 40em; margin: 0 auto; color: #222; background: #fdfcf8; }
.ctx  { font-family: -apple-system, sans-serif; font-size: 13px; color: #8a7a5a;
        text-transform: uppercase; letter-spacing: .04em; margin-bottom: .6em; }
.hide { color: #b5651d; font-weight: bold; }
.ans  { color: #1d5fb5; }
.step { font-family: -apple-system, sans-serif; font-size: 11px; color: #aaa; margin-top: 1.5em; }
.nightMode .card, .card.nightMode { color: #ddd; background: #1e1e1e; }
.nightMode .ans { color: #7fb2ff; } .nightMode .hide { color: #f0a050; }
"""


def write_apkg(cards, path):
    import genanki
    model = genanki.Model(
        1607392319, "SOM Progression Prototype",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Step"}],
        templates=[{"name": "Card 1",
                    "qfmt": "{{Front}}<div class='step'>{{Step}}</div>",
                    "afmt": "{{Back}}<div class='step'>{{Step}}</div>"}],
        css=CSS)
    deck = genanki.Deck(2059400110, "Sermon on the Mount (progression prototype)")
    for c in cards:
        deck.add_note(genanki.Note(
            model=model,
            fields=[to_html(c.front), to_html(c.back),
                    html.escape(f"#{c.pos} · step {c.step} · {c.kind} · unit {c.unit + 1}")],
            tags=[f"step::{c.step}", f"unit::{c.unit + 1:02d}"],
            guid=genanki.guid_for("som-proto", c.pos), due=c.pos))
    genanki.Package(deck).write_to_file(path)

# --------------------------------------------------------------------------
# Review simulation (simplified Anki SM-2, Good/Again only)
# --------------------------------------------------------------------------

LEARN_STEPS = [0, 0, 1, 3]       # 1m, 10m, 1d, 3d (minute steps = same day)
GRAD_IVL, START_EASE = 7, 2.5
FAIL = {"P": .10, "A": .12, "F": .18, "B": .25, "C": .25, "D": .30}  # learning
REVIEW_FAIL = .10


def simulate(cards, new_per_day, days, seed=7):
    rng = random.Random(seed)
    state = {c.pos: None for c in cards}  # None = new
    rows, summary = [], []
    new_queue = list(cards)
    by_pos = {c.pos: c for c in cards}
    for day in range(1, days + 1):
        due = sorted((s["due"], p) for p, s in state.items() if s and s["due"] <= day)
        today = [(p, "review" if state[p]["q"] == "rev" else "learning") for _, p in due]
        intro = new_queue[:new_per_day]
        new_queue = new_queue[new_per_day:]
        for c in intro:
            state[c.pos] = {"q": "learn", "step": 0, "due": day, "ivl": 0, "ease": START_EASE}
        today += [(c.pos, "new") for c in intro]
        seq, later = 0, []
        queue = list(today)
        n_new = len(intro)
        n_rev = sum(1 for _, k in today if k != "new")
        while queue:
            p, kind = queue.pop(0)
            c, s = by_pos[p], state[p]
            fail_p = REVIEW_FAIL if s["q"] == "rev" else FAIL[c.step] * (0.5 if kind == "again today" else 1)
            failed = kind != "new" and rng.random() < fail_p
            if s["q"] == "rev":
                if failed:
                    s.update(q="relearn", step=1, ease=max(1.3, s["ease"] - .2),
                             ivl=max(1, round(s["ivl"] * .2)))
                    queue.append((p, "again today"))
                    result, nxt = "again", day
                else:
                    s["ivl"] = max(s["ivl"] + 1, round(s["ivl"] * s["ease"]))
                    s["due"] = day + s["ivl"]
                    result, nxt = "good", s["due"]
            elif s["q"] == "relearn":
                if failed:
                    queue.append((p, "again today")); result, nxt = "again", day
                else:
                    s.update(q="rev", due=day + s["ivl"]); result, nxt = "good", s["due"]
            else:  # learning
                if failed:
                    s["step"] = 0
                else:
                    s["step"] += 1
                if s["step"] >= len(LEARN_STEPS):
                    s.update(q="rev", ivl=GRAD_IVL, due=day + GRAD_IVL)
                    result, nxt = "graduated", s["due"]
                elif LEARN_STEPS[s["step"]] == 0:
                    queue.append((p, "again today"))
                    result, nxt = ("again" if failed else "good"), day
                else:
                    s["due"] = day + LEARN_STEPS[s["step"]]
                    result, nxt = "good", s["due"]
            seq += 1
            rows.append({"day": day, "seq": seq, "shown_as": kind, "card_pos": p,
                         "step": c.step, "card_type": c.kind, "unit": c.unit + 1,
                         "section": c.node, "ref": c.ref, "front": to_plain(c.front),
                         "back": to_plain(c.back), "result": result, "next_due_day": nxt})
        shown = sum(1 for r in rows if r["day"] == day)
        units_new = sorted({c.unit + 1 for c in intro if c.step == "A"})
        summary.append({"day": day, "new_cards": n_new, "due_reviews": n_rev,
                        "total_shown_incl_repeats": shown,
                        "est_minutes": round(shown * 12 / 60, 1),
                        "new_steps": "".join(sorted({c.step for c in intro})),
                        "units_started": " ".join(map(str, units_new)),
                        "furthest_unit_started": max([c.unit + 1 for c in cards
                                                      if c.step == "A" and state[c.pos]], default="")})
    return rows, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new-per-day", type=int, default=12)
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()

    verses, index = load_matthew()
    with open(OUTLINE_PATH, encoding="utf-8") as f:
        outline = yaml.safe_load(f)
    root_spec = outline["Matthew"]["sections"]["The Sermon on the Mount"]
    root = build_tree(root_spec, "The Sermon on the Mount", index)
    units = build_units(root)
    b = Builder(verses, root, units)
    cards = b.build()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "units.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["unit", "ref", "verses", "sections", "keywords"])
        for u in units:
            w.writerow([u.idx + 1, b.ref(u.verses), len(u.verses),
                        " / ".join(s[0].title + s[2] for s in u.segments), b.kwchain(u.verses)])
    with open(OUT_DIR / "cards_in_order.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pos", "step", "card_type", "unit", "section", "ref", "front", "back"])
        for c in cards:
            w.writerow([c.pos, c.step, c.kind, c.unit + 1, c.node, c.ref,
                        to_plain(c.front), to_plain(c.back)])
    rows, summary = simulate(cards, args.new_per_day, args.days)
    for name, data in (("day_by_day.csv", rows), ("daily_summary.csv", summary)):
        with open(OUT_DIR / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            w.writeheader()
            w.writerows(data)
    write_apkg(cards, OUT_DIR / "som_progression_prototype.apkg")

    print(f"{len(units)} units, {len(cards)} cards -> {OUT_DIR}")
    print(Counter(c.step for c in cards))


if __name__ == "__main__":
    main()
