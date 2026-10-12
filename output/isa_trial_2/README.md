# Trial 2: Isaiah 40–44

Built by `src/deck/` from `data/outlines/isaiah_40_44.yml`, following [sequence v2](../../notes/sequence_v2_draft.md) (§11 has the build notes).

## Files

| File | What it is |
|---|---|
| `deck.apkg` | The Anki deck: 436 cards, one note each, in the planned order |
| `preview.html` | One card of each type, front and back. Open it in a browser to check the design. Night mode and type mode work there too |
| `cards_in_order.csv` | Every card with its position, planned day, phase, type and group |
| `units.csv` | The 44 units: leaf, part, verses, words |
| `daily_summary.csv` | New cards per day, by type |
| `fsrs_daily.csv` | Simulated reviews and minutes per day under FSRS (`scripts/simulate_fsrs.py`) |

## Setup in Anki

1. **Import `deck.apkg`.** Re-importing a rebuilt deck updates its cards in place.
2. **Give the deck its own options preset.** genanki can't carry deck options, so set these by hand (§6 of the draft):

   | Setting | Value |
   |---|---|
   | FSRS | On |
   | Desired retention | 0.90 |
   | Learning steps | `10m` |
   | Relearning steps | `10m` |
   | New cards/day | 12 |
   | Maximum reviews/day | 9999 |
   | New card gather order / sort order | Deck, then **Order gathered** |
   | Bury siblings | Off |

   New cards/day must match the build's `--per-day` (12), because "a day later" in the plan means 12 cards later.
3. **Test type mode on your phone** before day 5, the first Recite card. Tap "Type first letters" on a Recite card, type a few letters, and check that words appear and the score line updates.

## While you study

- Say every recall card aloud before flipping.
- Rate with the rubric on the back of each card. On Missing words and First letters cards, press Easy whenever it felt effortless.
- Keep notes as in trial 1. Note any card type where you press Again the first time you see a card: that step is too steep.
- **Checkpoints:** when Phase 1 ends (day 5), write the outline from memory. On days 30, 60 and 90, recite the whole text with only the outline as a cue.
- Each card is tagged `phase::1|2`, `type::<card type>`, `unit::uNN` or `section::<name>`, and `day::NN`, so the review log can be analysed by card type afterwards.
