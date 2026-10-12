"""
Simulate a v2 deck's daily workload under FSRS (py-fsrs), replacing trial 1's
SM-2 simulator for planning (notes/sequence_v2_draft.md §5).

    venv/bin/python scripts/simulate_fsrs.py output/isa_trial_2 [--days 120] [--runs 30]

Reads <dir>/cards_in_order.csv (written by `python -m src.deck`), introduces each
card on its planned day, and reviews whatever FSRS makes due, with the deck
options the draft recommends: desired retention 0.90, one 10-minute learning
step, one 10-minute relearning step. Writes <dir>/fsrs_daily.csv (means over runs).

Assumptions (estimates, not measurements -- trial 2's review log will replace them):
- A review succeeds with the recall probability FSRS predicts for it.
- Ratings follow the card rubric: reading cards are always Easy; scaffold cards
  (Missing words, First letters) are often Easy when recalled; a new recall card is
  usually Good because the card before it made it answerable.
- Seconds per review by card type are in SECONDS below.
- Cards are independent, as FSRS assumes; in reality reviewing one card of a verse
  helps its other cards, so this overstates the load somewhat (§6).
"""

import argparse
import csv
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fsrs import Card, Rating, Scheduler, State

SECONDS = {
    "read-through": 240, "preview": 20, "outline-cloze": 10, "list-parts": 25, "whole-outline": 90,
    "text-to-header": 20, "missing-words": 45, "first-letters": 45, "scaffolded-cloze": 25,
    "anchor-cloze": 40, "header-to-text": 50, "missing-section": 50, "first-lines": 40,
    "section-header-to-text": 120,
}
READING = {"read-through", "preview"}
SCAFFOLD = {"missing-words", "first-letters"}
# First rating of a brand-new card: (Again, Hard, Good, Easy) weights
FIRST = {"recall": (8, 12, 75, 5), "scaffold": (5, 10, 55, 30)}
START = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)  # every daily session starts at 09:00


def first_rating(kind: str, rng: random.Random) -> Rating:
    if kind in READING:
        return Rating.Easy
    weights = FIRST["scaffold" if kind in SCAFFOLD else "recall"]
    return rng.choices([Rating.Again, Rating.Hard, Rating.Good, Rating.Easy], weights)[0]


def later_rating(kind: str, recalled: bool, rng: random.Random) -> Rating:
    if kind in READING:
        return Rating.Easy
    if not recalled:
        return Rating.Again
    if kind in SCAFFOLD:
        return Rating.Easy if rng.random() < 0.6 else Rating.Good
    return rng.choices([Rating.Hard, Rating.Good, Rating.Easy], (10, 85, 5))[0]


def simulate(rows: list[dict], days: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    sched = Scheduler(desired_retention=0.9, learning_steps=(timedelta(minutes=10),),
                      relearning_steps=(timedelta(minutes=10),), enable_fuzzing=False)
    new_by_day = defaultdict(list)
    for r in rows:
        new_by_day[int(r["day"])].append(r)
    live: list[tuple[Card, str]] = []
    out = []
    for day in range(1, days + 1):
        t = START + timedelta(days=day - 1)
        session_end = t + timedelta(hours=4)
        reviews = seconds = 0
        due = [(c, k) for c, k in live if c.due <= t]
        live = [(c, k) for c, k in live if c.due > t]
        queue = due + [(Card(card_id=int(r["pos"]) + 1, due=t), r["type"]) for r in new_by_day[day]]
        while queue:
            queue.sort(key=lambda ck: ck[0].due)
            card, kind = queue.pop(0)
            t = max(t, card.due)
            if card.last_review is None:
                rating = first_rating(kind, rng)
            elif card.state != State.Review:  # a learning/relearning step: answered this session
                rating = Rating.Good
            else:
                recalled = rng.random() < sched.get_card_retrievability(card, t)
                rating = later_rating(kind, recalled, rng)
            card, _ = sched.review_card(card, rating, t)
            reviews += 1
            seconds += SECONDS[kind]
            t += timedelta(seconds=SECONDS[kind])
            (queue if card.due <= session_end else live).append((card, kind))
        out.append({"day": day, "new": len(new_by_day[day]), "reviews": reviews,
                    "minutes": seconds / 60})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck_dir", type=Path)
    ap.add_argument("--days", type=int, default=120)
    ap.add_argument("--runs", type=int, default=30)
    args = ap.parse_args()

    with open(args.deck_dir / "cards_in_order.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    runs = [simulate(rows, args.days, seed) for seed in range(args.runs)]
    mean = [{"day": d + 1, **{k: sum(run[d][k] for run in runs) / len(runs)
                              for k in ("new", "reviews", "minutes")}} for d in range(args.days)]

    with open(args.deck_dir / "fsrs_daily.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["day", "new", "reviews", "minutes"])
        w.writeheader()
        for m in mean:
            w.writerow({"day": m["day"], "new": round(m["new"]), "reviews": round(m["reviews"], 1),
                        "minutes": round(m["minutes"], 1)})

    last_new = max(int(r["day"]) for r in rows)
    peak = max(mean, key=lambda m: m["minutes"])
    def avg(a, b):
        span = [m["minutes"] for m in mean[a - 1:b]]
        return sum(span) / len(span) if span else 0.0
    print(f"{len(rows)} cards, new cards end on day {last_new}; {args.runs} runs averaged")
    print(f"Peak: day {peak['day']}, {peak['minutes']:.0f} min ({peak['reviews']:.0f} reviews)")
    for a, b in ((1, last_new), (last_new + 1, min(90, args.days)), (91, args.days)):
        if a <= b:
            print(f"  days {a}–{b}: {avg(a, b):.0f} min/day on average")
    print(f"Wrote {args.deck_dir / 'fsrs_daily.csv'}")


if __name__ == "__main__":
    main()
