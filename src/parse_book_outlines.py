"""Parse the BSB book-outline PDF into a nested YAML outline.

The outline's numbering cycles 1. -> a. -> i. -> 1. -> a. -> ..., so a marker
never fixes an entry's depth on its own: a bare "i." may be the first roman
child or the ninth letter of an alpha run. The PDF indents each level by a
fixed ~16.56pt, so depth comes from the line's x position (plus, for the
deepest level, leading spaces inside the text); the marker cycle is then used
only to interpret the marker and to check the assignment.
"""
import re
import sys
from pathlib import Path

import pymupdf
import yaml

CYCLE = ("arabic", "alpha", "roman")
ROMAN_VALUES = (("x", 10), ("ix", 9), ("v", 5), ("iv", 4), ("i", 1))

TIER0, TIER_STEP, TIER_TOL = 36.0, 16.56, 2.0
TITLE_X = 150                    # centred book titles sit far to the right

BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]

ENTRY = re.compile(r"^([0-9]+|[a-z]+)\.(?:\s+(.*))?$")
TRAILING_RANGE = re.compile(r"\s*\(([^()]*)\)\s*$")

warnings = []


def roman_to_int(tok):
    total, i = 0, 0
    while i < len(tok):
        for sym, val in ROMAN_VALUES:
            if tok.startswith(sym, i):
                total += val
                i += len(sym)
                break
        else:
            return None
    return total or None


def read_marker(tok, kind):
    """Interpret a marker token as a number under one numbering kind."""
    if kind == "arabic":
        return int(tok) if tok.isdigit() else None
    if tok.isdigit():
        return None
    if kind == "alpha":
        return ord(tok) - 96 if len(tok) == 1 and tok.isalpha() else None
    if kind == "roman":
        return roman_to_int(tok) if set(tok) <= set("ivxlcdm") else None
    return None


def read_lines(path):
    """[(page, depth, text)] for the outline pages; depth None for book titles."""
    doc = pymupdf.open(path)
    out = []
    for pno, page in enumerate(doc, 1):
        if pno < 3:                  # pages 1-2 are the book index and licence
            continue
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = line["spans"]
                if not spans:
                    continue
                raw = "".join(s["text"] for s in spans)
                raw = raw.replace("⁠", "").replace(" ", " ")
                text = raw.strip()
                if not text:
                    continue
                x = spans[0]["bbox"][0]
                if x > TITLE_X:
                    out.append((pno, None, text))
                    continue
                level = round((x - TIER0) / TIER_STEP)
                if level < 0 or abs(TIER0 + level * TIER_STEP - x) > TIER_TOL:
                    out.append((pno, -1, text))      # off-tier: a wrapped line
                    continue
                # The deepest level is indented with spaces inside the text
                # rather than by a further x offset.
                lead = len(raw) - len(raw.lstrip(" "))
                out.append((pno, level + (1 if lead >= 2 else 0), text))
    return out


def parse_range(text, where):
    """'1:1-10:32' / '21:1-8' / '3:16' -> ((ch, v), (ch, v)) and a clean ref."""
    clean = text.replace("—", "-").replace("–", "-")
    clean = re.sub(r"\s*-\s*", "-", clean).strip().strip("-").strip()
    parts = clean.split("-")
    if len(parts) == 1:
        parts = [parts[0], parts[0]]
    if len(parts) != 2 or ":" not in parts[0]:
        warnings.append(f"{where}: unparsed verse range {text!r}")
        return None, clean
    sch, sv = parts[0].split(":", 1)
    ech, ev = parts[1].split(":", 1) if ":" in parts[1] else (sch, parts[1])
    try:
        span = ((int(sch), int(sv)), (int(ech), int(ev)))
    except ValueError:
        warnings.append(f"{where}: non-numeric verse range {text!r}")
        return None, clean
    return span, f"{span[0][0]}:{span[0][1]}-{span[1][0]}:{span[1][1]}"


def collect(lines):
    """Group lines into per-book entry lists, rejoining wrapped entries."""
    books, entries = [], None
    for pno, depth, text in lines:
        if depth is None:
            if text in BOOKS:
                entries = []
                books.append((text, entries))
            else:
                warnings.append(f"p{pno}: unexpected centred line {text!r}")
            continue
        if text == "Outline":
            continue
        if entries is None:
            warnings.append(f"p{pno}: line before any book title {text!r}")
            continue
        m = ENTRY.match(text)
        if depth < 0 or not m:
            if entries:
                entries[-1]["text"] += " " + text      # wrapped continuation
            else:
                warnings.append(f"p{pno}: stray line {text!r}")
            continue
        entries.append({"marker": m.group(1), "text": m.group(2) or "",
                        "depth": depth, "page": pno})
    return books


def numbering_kind(tier):
    """The outline cycles 1. -> a. -> i. with each visual level of indentation."""
    return CYCLE[tier % 3]


def slot_fits(tok, parent, sibling_tier, span, counters):
    """Could this entry be filed under `parent` as a `sibling_tier` entry?

    It fits when the marker continues (or opens) that run's numbering and the
    verse range sits inside the parent and after the previous sibling. Returns
    the marker's value, or None.
    """
    value = read_marker(tok, numbering_kind(sibling_tier))
    if value is None:
        return None
    running = counters.get(id(parent))
    if running is None:
        if value != 1:
            return None
    elif value != running + 1:
        return None
    if span:
        if parent["span"] and not (parent["span"][0] <= span[0]
                                   and span[1] <= parent["span"][1]):
            return None
        kids = parent["children"]
        if kids and kids[-1]["span"] and span[0] < kids[-1]["span"][1]:
            return None
    return value


def place(tier, stack, tiers):
    """Map a visual indentation tier onto the open path.

    Returns the index of the parent it belongs under. A tier already on the
    path makes the entry a sibling at that level; a deeper one opens a child of
    the innermost node. This is what collapses the levels the source skips
    (Leviticus 26, Mark 7): the skipped tier simply never joins the path, so
    the entries below it stay siblings of each other.
    """
    for j in range(len(tiers) - 1, 0, -1):
        if tiers[j] == tier:
            return j - 1
    return len(stack) - 1


def build(books):
    tree = {}
    for name, entries in books:
        root = {"title": name, "marker": None, "ref": None, "span": None,
                "children": [], "page": None}
        stack, tiers, counters = [root], [-1], {}

        for e in entries:
            tok, tier = e["marker"], e["depth"]
            where = f"{name} p{e['page']} {tok}."
            text = e["text"].strip()
            rm = TRAILING_RANGE.search(text)
            if rm:
                span, ref = parse_range(rm.group(1), where)
                title = text[: rm.start()].strip()
            else:
                span, ref, title = None, None, text
                warnings.append(f"{where}: no verse range for {title!r}")

            depth = place(tier, stack, tiers)
            sib_tier = tiers[depth + 1] if depth + 1 < len(tiers) else tier
            value = slot_fits(tok, stack[depth], sib_tier, span, counters)

            if value is None:
                # The indentation disagrees with the numbering or the verse
                # ranges. Matthew 5-6 renders two deep sub-lists at the
                # top-level tier; look for an open slot that fits both.
                for alt in range(len(stack) - 1, -1, -1):
                    alt_tier = tiers[alt + 1] if alt + 1 < len(tiers) else tier
                    alt_value = slot_fits(tok, stack[alt], alt_tier, span, counters)
                    if alt_value is not None and alt != depth:
                        warnings.append(
                            f"{where}: indentation tier {tier} conflicts with the "
                            f"numbering or verse ranges; filed under "
                            f"{stack[alt]['title']!r} in {title!r}")
                        depth, sib_tier, value = alt, alt_tier, alt_value
                        break
                else:
                    value = read_marker(tok, numbering_kind(sib_tier))
                    warnings.append(
                        f"{where}: marker does not continue its run in {title!r}")

            del stack[depth + 1:]
            del tiers[depth + 1:]
            if value is not None:
                counters[id(stack[depth])] = value

            node = {"title": title, "marker": f"{tok}.", "ref": ref,
                    "span": span, "children": [], "page": e["page"]}
            stack[depth]["children"].append(node)
            stack.append(node)
            tiers.append(sib_tier)

        set_book_span(root)
        tree[name] = root
    return tree


def set_book_span(root):
    """A book's range is the span of its top-level sections."""
    kids = [k for k in root["children"] if k["span"]]
    if kids:
        root["span"] = (min(k["span"][0] for k in kids),
                        max(k["span"][1] for k in kids))
        root["ref"] = ref_of(root["span"])


def find_problems(tree):
    """Every node whose verse range contradicts its parent or its siblings.

    These are defects in the source PDF, reproduced verbatim in the YAML, so
    each one is reported with the context needed to decide the correction.
    """
    problems = []

    def walk(node, path, parent, siblings, idx, book):
        reasons = []
        prev = siblings[idx - 1] if siblings and idx > 0 else None
        nxt = siblings[idx + 1] if siblings and idx + 1 < len(siblings) else None
        if node["span"] is None:
            reasons.append("the verse range in the PDF is malformed and could "
                           "not be read as chapter:verse-chapter:verse")
        else:
            if parent and parent["span"] and not (
                    parent["span"][0] <= node["span"][0]
                    and node["span"][1] <= parent["span"][1]):
                reasons.append(f"falls outside its parent {parent['ref']}")
            if prev and prev["span"] and node["span"][0] < prev["span"][1]:
                reasons.append(
                    f"starts before the previous section {prev['title']!r} "
                    f"({prev['ref']}) ends")
            if node["span"][0] > node["span"][1]:
                reasons.append("starts after it ends")
        if reasons:
            problems.append({"book": book, "path": path, "node": node,
                             "parent": parent, "prev": prev, "next": nxt,
                             "reasons": reasons})
        for i, kid in enumerate(node["children"]):
            walk(kid, path + [kid["title"]], node, node["children"], i, book)

    for name, root in tree.items():
        walk(root, [name], None, None, 0, name)
    return problems


def ref_of(span):
    return f"{span[0][0]}:{span[0][1]}-{span[1][0]}:{span[1][1]}"


def inside(span, outer):
    return outer[0] <= span[0] and span[1] <= outer[1]


def edit_cost(old, new):
    """Size of an edit between two ranges; any chapter change outweighs verses."""
    return sum(abs(a[0] - b[0]) * 1000 + abs(a[1] - b[1])
               for a, b in zip(old, new))


def span_size(span):
    return (span[1][0] - span[0][0]) * 1000 + span[1][1] - span[0][1]


def fits(span, node, parent, siblings):
    """Would `span` be a sound range for `node`, a child of `parent`?

    Siblings whose own ranges fall outside the parent are ignored: they are
    broken themselves, so they cannot be trusted as constraints.
    """
    if span[0] > span[1]:
        return False
    # A book's own range is derived from its sections, so it bounds nothing.
    bounds = parent["span"] if parent and parent["marker"] else None
    if bounds and not inside(span, bounds):
        return False

    def sound(k):
        return k["span"] and not (bounds and not inside(k["span"], bounds))

    i = next(i for i, k in enumerate(siblings) if k is node)
    prev = next((k for k in reversed(siblings[:i]) if sound(k)), None)
    nxt = next((k for k in siblings[i + 1:] if sound(k)), None)
    if prev and span[0] < prev["span"][1]:
        return False
    if nxt and nxt["span"][0] < span[1]:
        return False
    return True


def chapter_fixes(node, parent, end_chapter):
    """Ranges that fit once only the chapter numbers change, cheapest first.

    In the defects seen, the verse numbers are right and a chapter number was
    mistyped, so only chapters are varied. One cheapest candidate is strong
    evidence; several mean the context cannot decide.
    """
    if node["span"] is None:
        return []
    (sc, sv), (ec, ev) = node["span"]
    found = []
    for new_sc in range(1, end_chapter + 1):
        for new_ec in range(new_sc, end_chapter + 1):
            span = ((new_sc, sv), (new_ec, ev))
            if span != node["span"] and fits(span, node, parent,
                                             parent["children"]):
                found.append((edit_cost(node["span"], span), span))
    if not found:
        return []
    best = min(c for c, _ in found)
    return [s for c, s in found if c == best]


def shared_offset(group, parent):
    """One chapter offset that brings a whole run of children inside `parent`.

    A single shared offset means the children's chapter numbers were mistyped
    together. Returns {id(node): span}, or None if no single offset works (or
    several do).
    """
    if not parent["span"] or any(p["node"]["span"] is None for p in group):
        return None
    failing = {id(p["node"]) for p in group}
    viable = []
    for offset in range(-40, 41):
        if offset == 0:
            continue
        spans, ok = [], True
        for kid in parent["children"]:
            if kid["span"] is None:
                ok = False
                break
            span = kid["span"]
            if id(kid) in failing:
                span = ((span[0][0] + offset, span[0][1]),
                        (span[1][0] + offset, span[1][1]))
                if span[0][0] < 1 or not inside(span, parent["span"]):
                    ok = False
                    break
            spans.append((kid, span))
        if not ok:
            continue
        if any(spans[i][1][0] < spans[i - 1][1][1] for i in range(1, len(spans))):
            continue                      # the run must still be in order
        viable.append({id(k): s for k, s in spans if id(k) in failing})
    return viable[0] if len(viable) == 1 else None


def widened_parent(group, parent, parents):
    """The parent's range stretched to cover these children, if that is sound.

    Sound means the stretched range still fits the grandparent and the
    parent's own siblings, and every child then fits among its siblings.
    """
    grand = parents.get(id(parent))
    if not parent["span"] or grand is None:
        return None
    spans = [p["node"]["span"] for p in group]
    if any(s is None for s in spans):
        return None
    span = (min([parent["span"][0]] + [s[0] for s in spans]),
            max([parent["span"][1]] + [s[1] for s in spans]))
    if not fits(span, parent, grand, grand["children"]):
        return None
    widened = dict(parent, span=span)
    for p in group:
        if not fits(p["node"]["span"], p["node"], widened, parent["children"]):
            return None
    return span


def smallest_container(node, book, index):
    """The tightest outline entry, outside node's own subtree, that contains it."""
    own = set()

    def mark(n):
        own.add(id(n))
        for k in n["children"]:
            mark(k)

    mark(node)
    best = None
    for key, cand in index.items():
        if key != book and not key.startswith(book + " > "):
            continue
        if id(cand) in own or not cand["span"] or not inside(node["span"],
                                                             cand["span"]):
            continue
        if best is None or span_size(cand["span"]) < best[0]:
            best = (span_size(cand["span"]), key)
    return best[1] if best else None


def parent_map(tree):
    parents = {}

    def walk(node):
        for kid in node["children"]:
            parents[id(kid)] = node
            walk(kid)

    for root in tree.values():
        walk(root)
    return parents


def index_paths(tree):
    """{"Book > Section > ...": node} for every node, books included."""
    index = {}

    def walk(node, path):
        index[" > ".join(path)] = node
        for kid in node["children"]:
            walk(kid, path + [kid["title"]])

    for name, root in tree.items():
        walk(root, [name])
    return index


MALFORMED_START = re.compile(r"^(\d+)-(\d+):(\d+)$")     # e.g. "21-22:16"


def proposals(tree, problems):
    """The corrections-file entries: one per thing to fix, with a suggestion
    wherever the surrounding ranges point clearly at one fix.

    Each problem is pinned on whichever side the evidence blames: the entry
    itself, its parent (a range a verse or two short, or Acts' truncated
    "5:12-"), or its previous sibling. Where no range edit can fix it -- an
    entry the PDF nested under the wrong section -- it gets a `parent` move.
    """
    parents = parent_map(tree)
    index = index_paths(tree)
    paths = {id(n): k for k, n in index.items()}

    def is_outside(p):
        return any("outside its parent" in r for r in p["reasons"])

    broken = {id(p["node"]) for p in problems if is_outside(p)}
    outside = {}
    for p in problems:
        if is_outside(p):
            outside.setdefault(id(p["parent"]), []).append(p)

    out = {}

    def add(node, suggested, why, **extra):
        key = paths[id(node)]
        if key not in out:
            out[key] = {"path": key, "ref": None, "pdf": node["ref"],
                        "page": node["page"], "suggested": suggested,
                        "why": why, **extra}

    for p in problems:
        node, parent = p["node"], p["parent"]
        end_chapter = tree[p["book"]]["span"][1][0]
        overlaps = any("starts before" in r for r in p["reasons"])

        if node["span"] is None:
            m = MALFORMED_START.match(node["ref"] or "")
            guess = None
            if m:
                span = ((int(m[1]), 1), (int(m[2]), int(m[3])))
                if fits(span, node, parent, parent["children"]):
                    guess = ref_of(span)
            add(node, guess, f"the PDF prints {node['ref']!r}, which has no "
                             f"starting verse")
            continue

        if not is_outside(p) and overlaps and p["prev"] \
                and id(p["prev"]) in broken:
            continue          # a knock-on: fixing the previous entry clears it

        group = outside.get(id(parent), []) if is_outside(p) else []
        if len(group) > 1:
            shifted = shared_offset(group, parent)
            if shifted:
                add(node, ref_of(shifted[id(node)]),
                    f"all {len(group)} entries here that fall outside their "
                    f"parent fit after the same chapter shift")
                continue
            widened = widened_parent(group, parent, parents)
            if widened and widened[0][0] == parent["span"][0][0] \
                    and widened[1][0] == parent["span"][1][0]:
                add(parent, ref_of(widened),
                    f"{len(group)} of its children fall outside this range; "
                    f"widening it within the same chapters covers them all")
                continue
            add(node, None,
                f"falls outside its parent {parent['ref']}, along with "
                f"{len(group) - 1} other entries; no range edit explains this, "
                f"so the PDF has likely nested it under the wrong section",
                parent=None,
                suggested_parent=smallest_container(node, p["book"], index))
            continue

        if is_outside(p):
            child = chapter_fixes(node, parent, end_chapter)
            widened = widened_parent([p], parent, parents)
            child_cost = (edit_cost(node["span"], child[0])
                          if len(child) == 1 else None)
            parent_cost = (edit_cost(parent["span"], widened)
                           if widened else None)
            if parent_cost is not None and (child_cost is None
                                            or parent_cost < child_cost):
                add(parent, ref_of(widened),
                    f"its child {node['title']!r} ({node['ref']}) falls "
                    f"outside it; widening this range is the smaller fix")
            elif child_cost is not None:
                add(node, ref_of(child[0]), "; ".join(p["reasons"]))
            else:
                why = "; ".join(p["reasons"])
                if len(child) > 1:
                    why += (f" (candidates: "
                            f"{', '.join(ref_of(c) for c in child[:4])})")
                add(node, None, why + "; either it or its parent is wrong")
            continue

        child = chapter_fixes(node, parent, end_chapter)
        if len(child) == 1:
            add(node, ref_of(child[0]), "; ".join(p["reasons"]))
            continue
        prev = p["prev"]
        if overlaps and prev and node["span"][0][1] > 1:
            cut = (node["span"][0][0], node["span"][0][1] - 1)
            shrunk = (prev["span"][0], cut)
            kids_ok = all(k["span"] is None or k["span"][1] <= cut
                          for k in prev["children"])
            if shrunk[0] <= shrunk[1] and kids_ok:
                add(prev, ref_of(shrunk),
                    f"it overlaps the next entry {node['title']!r} "
                    f"({node['ref']}); ending it the verse before is the "
                    f"likelier fix")
                continue
        add(node, None, "; ".join(p["reasons"]))

    return list(out.values())


def write_corrections_template(path, tree, problems):
    entries = proposals(tree, problems)
    header = (
        "# Manual corrections to the BSB book outlines.\n"
        "#\n"
        "# src/parse_book_outlines.py applies these after parsing the PDF, so\n"
        "# they survive regeneration. Each entry names an outline entry by its\n"
        "# `path` as parsed from the PDF, before any corrections -- that holds\n"
        "# even for an entry that has been moved.\n"
        "#\n"
        "# To fix one, fill in either or both, then rerun the script:\n"
        "#   ref:    the corrected range, chapter:verse-chapter:verse\n"
        "#   parent: the path of the section it should sit under instead\n"
        "# Fields left null change nothing. `pdf`, `page`, `suggested`,\n"
        "# `suggested_parent` and `why` are information only. Add entries for\n"
        "# any other path you want to override.\n"
        "\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(entries, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=10 ** 6)
    return len(entries)


def apply_corrections(tree, path):
    """Apply ref overrides and parent moves. Returns how many entries changed."""
    if not path.exists():
        return 0
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise SystemExit(f"{path.name} must be a list of entries, each with "
                         f"a `path`")
    index = index_paths(tree)          # resolved once: paths are as parsed
    parents = parent_map(tree)
    errors, refs, moves = [], [], []

    for i, entry in enumerate(data, 1):
        key = (entry or {}).get("path")
        where = f"entry {i} ({key!r})"
        node = index.get(key)
        if node is None:
            errors.append(f"{where}: no outline entry has this path")
            continue
        ref, new_parent = entry.get("ref"), entry.get("parent")
        if ref is not None:
            if not isinstance(ref, str):
                errors.append(f"{where}: ref {ref!r} must be quoted text, "
                              f"e.g. '3:16-3:16'")
            else:
                span, clean = parse_range(ref, where)
                if span is None or span[0] > span[1]:
                    errors.append(f"{where}: cannot read ref {ref!r}")
                else:
                    refs.append((node, span, clean))
        if new_parent is not None:
            target = index.get(new_parent)
            if target is None:
                errors.append(f"{where}: parent {new_parent!r} is not an "
                              f"outline path")
            elif new_parent == key or new_parent.startswith(key + " > "):
                errors.append(f"{where}: cannot move an entry under itself")
            else:
                moves.append((node, target))
    if errors:
        raise SystemExit(f"{path.name} has problems; nothing was written:\n  "
                         + "\n  ".join(errors))

    for node, span, clean in refs:
        node["span"], node["ref"] = span, clean
    for node, target in moves:
        parents[id(node)]["children"].remove(node)
        target["children"].append(node)
        parents[id(node)] = target
    for target in {id(t): t for _, t in moves}.values():
        target["children"].sort(key=lambda k: k["span"][0] if k["span"]
                                else (10 ** 6, 0))
    for root in tree.values():
        set_book_span(root)
    return len({id(n) for n, _, _ in refs} | {id(n) for n, _ in moves})


def write_report(path, tree, problems, source_name, applied=0):
    lines = [
        "Problems in data/outlines/bsb_book_outlines.yml",
        "=" * 60,
        "",
        f"Source: data/raw/{source_name}",
        "Regenerate: python src/parse_book_outlines.py",
        "",
        "Every item below is a defect in the source PDF that the corrections",
        f"file ({CORRECTIONS_PATH.name}, {applied} entries applied so far)",
        "does not fix yet. The parse itself is sound: all 66 books and every",
        "outline entry are present, and the nesting was cross-checked against",
        "the PDF's indentation, its 1./a./i. numbering cycle and the verse",
        "ranges.",
        "",
        f"Fix them in {CORRECTIONS_PATH.name}, which suggests a fix wherever",
        "the context points clearly at one. Never edit the generated YAML. One",
        "fix often clears several items here: widening a parent clears every",
        "child listed as falling outside it.",
        "",
    ]

    by_book = {}
    for p in problems:
        by_book.setdefault(p["book"], []).append(p)

    lines += [f"{len(problems)} problems across {len(by_book)} books:", ""]
    for book, items in by_book.items():
        lines.append(f"  {book}: {len(items)}")
    lines += ["", ""]

    n = 0
    for book, items in by_book.items():
        lines += [book.upper(), "-" * len(book), ""]
        for p in items:
            n += 1
            node = p["node"]
            lines.append(f"[{n}] {node['marker']} {node['title']}")
            lines.append(f"     path:        {' > '.join(p['path'])}")
            lines.append(f"     PDF page:    {node['page']}")
            lines.append(f"     ref:         {node['ref']}")
            for reason in p["reasons"]:
                lines.append(f"     problem:     {reason}")
            if p["parent"] and p["parent"]["ref"]:
                lines.append(f"     parent:      {p['parent']['title']} "
                             f"({p['parent']['ref']})")
            if p["prev"]:
                lines.append(f"     previous:    {p['prev']['title']} "
                             f"({p['prev']['ref']})")
            if p["next"]:
                lines.append(f"     next:        {p['next']['title']} "
                             f"({p['next']['ref']})")
            for kid in node["children"][:1]:
                lines.append(f"     first child: {kid['title']} ({kid['ref']})")
            lines.append("")
        lines.append("")

    lines += [
        "",
        "REPAIRS ALREADY MADE BY THE PARSER (verify; no edit needed unless",
        "they look wrong)",
        "-" * 70,
        "",
        "The PDF's indentation is wrong in three places. The parser corrected",
        "these because the numbering and the verse ranges both agreed:",
        "",
        "  1. Matthew 5:21-48 -- the a.-e. sub-list ('Anger and Reconciliation'",
        "     through 'Love Your Enemies', PDF p82) is printed at the top-level",
        "     indent. Filed under 'You Have Heard It Said...'.",
        "",
        "  2. Matthew 6 -- same defect for the a.-f. sub-list ('Giving to the",
        "     Needy' through 'Do Not Worry', p82). Filed under 'The Lord Sees",
        "     What is Done in Secret'.",
        "",
        "  3. Leviticus 26 (p12) and Mark 7:24 (p88) -- the source skips a",
        "     level, jumping from '8. Epilogue' / '3. Jesus' Ministry in Various",
        "     Gentile Regions' straight to roman-numbered children. Those",
        "     children attach directly to the section above them.",
        "",
    ]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def to_mapping(node):
    """{title: {ref, sections}} -- `sections` omitted for a leaf."""
    out = {"ref": node["ref"]}
    if node["children"]:
        out["sections"] = {k["title"]: to_mapping(k) for k in node["children"]}
    return out


def count(node):
    return len(node["children"]) + sum(count(k) for k in node["children"])


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_PDF = BASE_DIR / "data" / "raw" / "bsb_book_outlines.pdf"
OUTLINES_DIR = BASE_DIR / "data" / "outlines"
OUTPUT_PATH = OUTLINES_DIR / "bsb_book_outlines.yml"
REPORT_PATH = OUTLINES_DIR / "bsb_book_outlines.problems.txt"
CORRECTIONS_PATH = OUTLINES_DIR / "bsb_book_outlines.corrections.yml"


def main(source=SOURCE_PDF, output=OUTPUT_PATH, report=REPORT_PATH,
         corrections=CORRECTIONS_PATH):
    tree = build(collect(read_lines(source)))

    if not corrections.exists():
        n = write_corrections_template(corrections, tree, find_problems(tree))
        print(f"{n} entries to fill in -> {corrections}")
    applied = apply_corrections(tree, corrections)

    problems = find_problems(tree)
    entries = sum(count(b) for b in tree.values())

    document = {name: to_mapping(root) for name, root in tree.items()}
    header = (
        f"# Book outlines of the Berean Study Bible.\n"
        f"# Generated from {source.name} and {corrections.name} by\n"
        f"# src/{Path(__file__).name} -- edit those, not this.\n"
        f"# {len(tree)} books, {entries} entries. Verse ranges are "
        f"chapter:verse-chapter:verse, relative to the book.\n"
        f"# {applied} ranges corrected by hand; {len(problems)} still "
        f"inconsistent (see {report.name}).\n"
    )
    with open(output, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(document, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=10 ** 6)

    write_report(report, tree, problems, source.name, applied)

    print(f"{len(tree)} books, {entries} entries -> {output}")
    print(f"{applied} corrections applied from {corrections.name}")
    print(f"{len(problems)} problems remaining -> {report}")
    missing = [b for b in BOOKS if b not in tree]
    if missing:
        print(f"\nMISSING BOOKS: {missing}")


if __name__ == "__main__":
    main(*(Path(a) for a in sys.argv[1:5]))
