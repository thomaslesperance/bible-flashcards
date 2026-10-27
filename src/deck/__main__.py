"""
Build a v2 deck from an outline.

    venv/bin/python -m src.deck data/outlines/isaiah_40_44.yml \
        --name "Isaiah 40–44 (trial 2)" --out output/isa_trial_2 [--per-day 12]

Writes <out>/deck.apkg, cards_in_order.csv, units.csv, daily_summary.csv and
preview.html (one card of each type, front and back, for checking the design
in a browser), then prints the counts and the spacing the plan achieved.
"""

import argparse
import csv
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

from ..db import fetch_one
from .anki import ASSETS, write_package
from .cards import CardBuilder
from .order import Planner, Placed
from .tree import load_tree


def credit_line(translation: str) -> str:
    row = fetch_one("SELECT englishName, licenseNotice FROM Translation WHERE id = ?", (translation,))
    if row is None:
        return translation
    notice = " ".join((row["licenseNotice"] or "").split())
    return f"Scripture: {row['englishName']} ({translation}). {notice}".strip()


def write_csvs(out: Path, placed: list[Placed], root) -> None:
    with open(out / "cards_in_order.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pos", "day", "phase", "type", "group", "key", "about"])
        for p in placed:
            w.writerow([p.pos, p.day, p.card.phase, p.card.kind, p.group, p.card.key, p.card.about])
    with open(out / "units.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["unit", "leaf", "part", "ref", "verses", "words"])
        for n in root.walk():
            for u in n.units:
                w.writerow([u.key, n.title, f"{u.index + 1}/{u.count}", u.ref, len(u.verses), u.words])
    kinds = sorted({p.card.kind for p in placed}, key=[p.card.kind for p in placed].index)
    by_day = defaultdict(Counter)
    for p in placed:
        by_day[p.day][p.card.kind] += 1
    with open(out / "daily_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["day", "new"] + kinds)
        for day in sorted(by_day):
            w.writerow([day, sum(by_day[day].values())] + [by_day[day][k] for k in kinds])


def write_preview(out: Path, placed: list[Placed], title: str) -> None:
    css = (ASSETS / "card.css").read_text(encoding="utf-8")
    js = (ASSETS / "card.js").read_text(encoding="utf-8")
    seen, sections = set(), []
    for p in placed:
        c = p.card
        if c.kind in seen:
            continue
        seen.add(c.kind)
        sections.append(
            f'<section><h2>{escape(c.kind)} <small>· day {p.day} · {escape(c.about)}</small></h2>'
            f'<div class="pair"><div><h3>Front</h3><div class="card">{c.front}</div></div>'
            f'<div><h3>Back</h3><div class="card">{c.back}</div></div></div></section>')
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · card preview</title>
<style>
{css}
body {{ margin: 0; padding: 16px; background: #ecebe6; font-family: system-ui, sans-serif; }}
body.dark {{ background: #111114; color: #ddd; }}
h1 {{ font-size: 1.2rem; }} h2 {{ font-size: 1rem; margin: 2rem 0 .5rem; }}
h2 small {{ font-weight: 400; color: #777; }} h3 {{ font: 600 .75rem system-ui; color: #888; margin: .3rem 0; }}
.pair {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
.pair .card {{ border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,.15); }}
</style></head>
<body>
<h1>{escape(title)} — one card of each type</h1>
<p><button onclick="document.body.classList.toggle('dark');document.querySelectorAll('.card').forEach(function(c){{c.classList.toggle('nightMode')}})">Toggle night mode</button>
 Type mode works here too: try the Recite card's buttons.</p>
{''.join(sections)}
<script>
{js}
</script>
</body></html>"""
    (out / "preview.html").write_text(page, encoding="utf-8")


def report(placed: list[Placed], root, per_day: int) -> None:
    kinds = Counter(p.card.kind for p in placed)
    phase = Counter(p.card.phase for p in placed)
    print(f"Headers: {root.header_count()}   Units: {sum(len(n.units) for n in root.walk())}   "
          f"Verses: {len(root.verses)}   Words: {root.words}")
    print(f"Cards: {len(placed)} (Phase 1: {phase[1]}, Phase 2: {phase[2]})   "
          f"Days at {per_day}/day: {placed[-1].day}")
    for kind, n in kinds.items():
        print(f"  {kind:<24}{n:>4}")
    first_day = {}
    for p in placed:
        first_day.setdefault(p.group, p.day)
    gaps = {"1→2": [], "2→3": []}
    for g, day in first_day.items():
        if g.startswith("wave 2 · "):
            u = g.removeprefix("wave 2 · ")
            gaps["1→2"].append(day - first_day[f"wave 1 · {u}"])
            gaps["2→3"].append(first_day[f"wave 3 · {u}"] - day)
    for name, gs in gaps.items():
        print(f"  waves {name}: {sum(g >= 1 for g in gs)} of {len(gs)} multi-verse units a day or more apart")
    last_p1 = max(p.day for p in placed if p.card.phase == 1)
    first_p2 = min(p.day for p in placed if p.card.phase == 2)
    print(f"  Phase 1 runs days 1–{last_p1}; text starts on day {first_p2}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outline", type=Path)
    ap.add_argument("--name", required=True, help="Anki deck name")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--per-day", type=int, default=12, help="new cards per day (N)")
    ap.add_argument("--translation", default="BSB")
    args = ap.parse_args()

    root, text = load_tree(args.outline, args.translation)
    credit = credit_line(args.translation)
    placed = Planner(root, CardBuilder(root, text, credit), args.per_day).plan()

    args.out.mkdir(parents=True, exist_ok=True)
    description = (f"Card sequence v2 (docs/method/sequence-v2.md). Set new cards/day to "
                   f"{args.per_day} and new card order to 'Order gathered'.<br><br>{escape(credit)}")
    write_package(placed, args.name, description, args.out / "deck.apkg")
    write_csvs(args.out, placed, root)
    write_preview(args.out, placed, args.name)
    report(placed, root, args.per_day)
    print(f"Wrote {args.out}/deck.apkg, CSVs and preview.html")


if __name__ == "__main__":
    main()
