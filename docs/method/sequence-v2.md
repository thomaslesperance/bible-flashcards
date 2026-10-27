# Card Sequence v2 (draft for review)

Revised after trial 1, a personal Anki trial of the Sermon on the Mount. The numbers come from a throwaway prototype run on `data/outlines/sermon_on_the_mount.yml` with the BSB text.

## Summary

- **Two phases.** Phase 1 learns the whole outline before any verse is drilled. Phase 2 learns the text unit by unit, from leaves to trunk.
- **Trial 1's nine-step sequence is the core.** v2 keeps it. It adds a few cards that present new material before testing it. It also adds timing and size rules, so the sequence works on any outline.
- **Every card shows where you are.** A map of the outline sits on the front and back of every card, except where your position is the answer.
- **The text keeps its shape.** Hidden words are blanked or blurred where they stand, so a passage looks the same on every card. The back reveals the answer in place.
- **Built for FSRS.** No card asks for something you haven't seen yet. "Again" on a new card therefore means a step is too steep. Each card carries a rating rubric, and there is one 10-minute learning step.
- **Sermon on the Mount:** 356 cards, 62 for the outline and 294 for the text (trial 1 had 385). At 12 new cards a day, the outline takes days 1–6 and the text runs from day 6 to day 30.

## Terms

- **Leaf**: a header with no sub-headers. It holds verses directly.
- **Section**: a header with sub-headers, or a leaf long enough to be split into parts. Its sub-headers or parts are its **parts**.
- **Unit**: the chunk of text learned as one piece. It is a leaf, or one part of a long leaf, about 4–6 verses (§4).
- **Map**: the outline drawn around the current item.

## 1. What changed, and why

| Trial 1 finding | v2 response |
|---|---|
| More work on the whole outline first, maybe not total recall | Phase 1 covers the full outline up front when it has 40 headers or fewer (the SOM has 34). It ends with whole-outline recall. Bigger outlines learn their top levels first and the rest just before each branch's text. |
| More surrounding lines in outline and sub-unit clozes | Outline cards show the **map**: the path from the top down to the item, every sibling at each level, and other branches collapsed to one line. Text clozes also show, dimmed, the verse just before and just after the unit. |
| "What section is this?" needs to stand out | It becomes a large banner. The back shows the answer large, with its place on the map. |
| First-letter cards look odd | Each letter sits where its word would be. The rest of the word is blurred in place, and the back un-blurs it where it stands. |
| Show the text's position in the outline when reciting | Every text card has a map strip on the front and the back. |
| Always pressing Again on new cards; why the 1m step? | Every new item is first presented (Read-through, Preview) or follows a card that makes it answerable. §6 answers the question. |
| A missing-words card to bridge the gap | **Missing words** (every 2nd and 3rd word blanked) sits between first exposure and first letters. |
| Liked the sub-unit text cloze in context | Kept at every level of the outline as **Missing section**. |
| Liked recalling the entire outline | **List the parts** for every section, plus **Whole outline** cards to finish Phase 1. |
| Produce output instead of guessing silently | Recite aloud on every recall card. An optional mode lets you type first letters, built with the card's JavaScript (§7). |

Dropped from trial 1:
- **Seam cards.** The dimmed neighbour verses and Missing section cards cover transitions.
- **Keyword cards.** Replaced by **First lines**: how does each part of a section begin?
- **Whole-section first letters.**

The reasoning behind the shape:
- **Map before territory.** People recall far more of a word list when it is shown as a hierarchy than when the same words come jumbled (Bower et al., 1969). The outline is that hierarchy for the text.
- **Withdraw cues one step at a time.** This is the "vanishing cues" method (Glisky, Schacter & Tulving, 1986). Each card is answerable from the one before, which also gives FSRS clean ratings.
- **Space the steps.** A unit's steps fall on three different days, not in one sitting.
- **Produce, don't just recognize** (§7).

## 2. The sequence at a glance

```
PHASE 1 · OUTLINE        top-down, one level at a time
  each top-level section      Read-through        read its text aloud once           new
  each section                Preview             the section and its parts shown     new
  each header                 Outline cloze       the map with one header blank       your #1, #2
  each section, a day later   List the parts      recall its parts in order           new
  sections with sub-sections  Whole outline       last card(s) of Phase 1             new

PHASE 2 · TEXT           reading order, leaves to trunk
  each unit   wave 1          Text → header                                           your #3
                              Missing words                                           your #4
                              First letters                                           your #5
              wave 2 (+1 day) Scaffolded cloze    one per verse; units of 2+ verses   your #6
                              Anchor cloze        units of 4+ verses                  your #7
              wave 3 (+1 day) Header → text                                           your #8
  each section, after its last unit's Header → text:
                              Missing section     one per part up to 280 words        your #9
                              First lines         sections over 280 words             new
              (+1 day)        Section header → text   sections up to 450 words        new
```

## 3. Phase 1: the outline

**Order:** breadth-first. The top level comes first (the Sermon's 5 movements), then each movement's parts, then theirs. Within a level, cards follow reading order.

**Cards for each section:**
1. **Read-through** (top-level sections only). "Read 5:3–16 aloud," with the full text beside its outline. It is a reading card, not a test: press Easy. It is the only verse text in Phase 1. It's here because the headers of an unfamiliar text mean little until you've read what they label (Decision 1).
2. **Preview.** The section and its parts, with verse ranges and nothing hidden. Press Easy.
3. **Outline cloze**, one per part. The map with that part's header blank. You can answer it because you just saw the Preview.
4. **List the parts**, about a day later. The map with this section's parts collapsed: "List its 4 parts."
5. **Whole outline.** For sections with sub-sections, once all of their own sections are done: "Recite the whole outline of Doing Right by Others (9 headers)." The last card of Phase 1 is the whole Sermon (34 headers).

**Any outline:**
- *Flat outlines.* BSB's own SOM outline has 20 sections under one header. Its Outline clozes still show the whole list, and List the parts is split into runs of 5.
- *Large outlines* (over 40 headers). Phase 1 covers as many top levels as fit in 40 headers. Each deeper section gets its Preview, Outline clozes, and List the parts just before that branch's text in Phase 2. That is your #2 ("current sub-unit outline cloze") in its natural place. The SOM fits, so all of its outline comes first.

Phase 2 starts once every Phase 1 card has been introduced.

**Outline cloze, front:**

```
OUTLINE · what goes in the blank?

The Sermon on the Mount
 1  The Beatitudes                        5:3–16   ▸ 4
 2  Doing Right by Others                 5:17–48
     a  Jesus Fulfills the Law            5:17–20
     b  Anger, Lust, and Remarriage       5:21–32
         i    Anger and Murder            5:21–26
         ii   ________________            5:27–30
         iii  Divorce and Remarriage      5:31–32
     c  Honesty, Pacifism, Perfect Love   5:33–48  ▸ 3
 3  Doing Right by God                    6:1–18   ▸ 3
 4  Doing Right by Others (continued)     6:19–7:12 ▸ 3
 5  The Choice                            7:13–27  ▸ 3
```

On the back, the blank fills in, highlighted. Verse ranges and collapsed counts (`▸ 3`) give orientation without giving the answer away.

## 4. Phase 2: the text

**Units.** Each leaf is one unit unless it runs over about 130 words (roughly 6 verses). A longer leaf is split at its paragraph breaks into parts of about 80 words. The SOM yields 30 units of 1–7 verses. For example, Anger and Murder becomes 5:21–23 and 5:24–26, and Prayer becomes 6:5–8 and 6:9–15. Small leaves are no longer merged with their neighbours as they were in trial 1, so each unit has exactly one place on the map. Sizes are in words because verse length varies a lot between books (Psalms versus Paul). At 21 words per BSB verse, 130 words is about 6 verses.

**The unit ladder:** three waves, a day apart.

| Wave | Card | Front | Notes |
|---|---|---|---|
| 1 | **Text → header** | Banner "Where does this belong?" and the unit's text | First drill of this text. Phase 1 makes it answerable. No map on the front, because position is the answer. The back shows the header large and its spot on the map. |
| 1 | **Missing words** | Map strip; every 2nd and 3rd word blanked, each blank as wide as its word | The back fills the words in place, tinted |
| 1 | **First letters** | Map strip; first letters in place, the rest of each word blurred | The back clears the blur in place |
| 2 | **Scaffolded cloze** | Map strip; one verse blurred as a block; dimmed verses before and after the unit | One card per verse; units of 2+ verses |
| 2 | **Anchor cloze** | First and last verses visible, the middle blurred | Units of 4+ verses |
| 3 | **Header → text** | Map strip with the unit highlighted: "Recite 5:21–23 (3 verses)" | A hint button shows first letters. Using it counts as Again. |

One-verse units skip wave 2.

**Section closing.** These cards come after the last unit of a section has had its Header → text, working up the tree, so inner sections close before outer ones.

| Card | Which sections | Front |
|---|---|---|
| **Missing section** | One card per part of up to 280 words | The section's text with one part blurred as a block, its header and verse range shown. If the section runs over 450 words, only the verse before and the verse after appear. |
| **First lines** | Sections over 280 words | The section's parts listed: "How does each one begin?" The back gives each part's opening words. |
| **Section header → text** | Sections up to 450 words, a day later | "Recite The Beatitudes (5:3–16)" |

280 words is about 13 verses, or 2 minutes aloud. 450 words is about 20 verses, or 3 minutes. Three SOM sections are larger than that: Doing Right by Others, its continuation, and the whole Sermon. They get no single recite card. You recite them through their parts, with First lines and the outline joining the parts. Reciting a whole movement from start to finish would happen outside the deck (Decision 4).

**Timing.** Anki introduces exactly N new cards per day, in deck order. "A day later" therefore has to be encoded as "N cards later." The generator follows four rules:
- Each wave lands at least N cards after the previous wave of the same unit.
- Cards whose wait is over are placed first, oldest first. Then the next unit starts.
- At most two units are in waves 1–2 at once. This keeps new text arriving at about 5 verses a day instead of in bursts.
- If nothing is ready, the oldest waiting card is pulled forward.

Here is the Beatitudes branch at 12 cards a day:

| | Day 6 | Day 7 | Day 8 | Day 9 | Day 11 | Day 12 |
|---|---|---|---|---|---|---|
| Triad 1 (5:3–5) | wave 1, wave 2 | wave 3 | | | | |
| Triad 2 (5:6–8) | wave 1 | wave 2 | wave 3 | | | |
| Triad 3 (5:9–12) | wave 1 (starts) | wave 1, wave 2 | wave 2 | wave 3 | | |
| Salt, Light, and City (5:13–16) | | wave 1 | wave 2 | wave 3 | | |
| **The Beatitudes** (section) | | | | | Missing section ×4 | Recite 5:3–16 |

Day 6 also carries the last two Whole outline cards. Triad 1 gets two waves on day 6 only because text is starting cold. Across the deck, 25 of 27 multi-verse units get at least a day between waves 1 and 2, and 25 of 27 between waves 2 and 3.

## 5. Size rules and counts for the SOM

| Rule | Default | SOM result |
|---|---|---|
| Unit size | target 80 words, max 130 | 30 units; 4 leaves split |
| Recite cap (Missing section, First lines threshold) | 280 words | |
| Context cap (Missing section shows all sibling text) | 450 words | |
| Long-recite cap (Section header → text) | 450 words | 11 sections get one |
| Outline up front | 40 headers | all 34 headers up front |
| List the parts, max per card | 7 headers, otherwise runs of 5 | not needed; the largest family has 5 |
| Units in waves 1–2 at once | 2 | |
| New cards/day (N) | 12 | 30 days in total |

| Phase 1 | | Phase 2 | |
|---|---:|---|---:|
| Read-through | 5 | Text → header | 30 |
| Preview | 10 | Missing words | 30 |
| Outline cloze | 34 | First letters | 30 |
| List the parts | 10 | Scaffolded cloze | 104 |
| Whole outline | 3 | Anchor cloze | 15 |
| | | Header → text | 30 |
| | | Missing section | 36 |
| | | First lines | 8 |
| | | Section header → text | 11 |
| **Total** | **62** | **Total** | **294** |

At 10 new cards a day, everything is introduced in 36 days. At 12 it takes 30, and at 15 it takes 24. Daily review load hasn't been simulated under FSRS yet. Trial 1's simulator ([simulate_progression.py](../scripts/simulate_progression.py)) used SM-2 and estimated 15–25 minutes a day at the peak for a similar number of cards. Before trial 2, the simulator should switch to FSRS (the `py-fsrs` package) so the estimate matches what you'll actually run.

## 6. Learning steps, FSRS, and how to rate

**Your question: is this why the first learning step is 1m?** Yes. Trial 1's package was built with genanki, which can't carry deck options, so Anki used your Default preset. Unless you changed it, its learning steps are `1m 10m`. A new card moves through them like this:
- **Again** sends it back to the first step: it returns in 1 minute. That's the "you just saw the answer, now retrieve it" step.
- **Good** moves it to the next step (10m). Good on the last step graduates the card.
- **Easy** graduates it immediately. **Hard** on the first step brings it back in about 6 minutes.

So the 1m step only applies after Again. A Good on a brand-new card skips it.

**Why this matters more under FSRS.** The first rating sets the card's starting *stability*: the number of days until your chance of recalling it falls to 90%. With default parameters it starts at roughly:
- Again: a few hours
- Hard: about a day
- Good: 2–3 days
- Easy: 1–2 weeks

Your optimized parameters will differ. Pressing Again on every new card starts every card weak. It also teaches FSRS that "Again on a new card" means nothing.

v2 is built so a new card can always be answered from the card before it:
- the Read-through and Preview come before the Outline clozes,
- Phase 1 comes before Text → header,
- each step of the text ladder removes only part of the cues.

If you press Again the first time you see a card, that card's step is too steep. Note the card type, and we'll adjust it.

**Recommended deck options (FSRS):**

| Setting | Value | Why |
|---|---|---|
| FSRS | On | |
| Desired retention | 0.90 | Anki's default balance between retention and workload |
| Learning steps | `10m` | The ladder already gives same-day repetition. Good on a new card graduates it; Again brings it back in 10 minutes. The Anki manual recommends few, short (under a day) steps with FSRS. |
| Relearning steps | `10m` | |
| New cards/day | 12 | The generator treats "a day later" as 12 cards later. Another value stretches or compresses the plan; it doesn't break it. |
| Maximum reviews/day | 9999 | Due reviews are never hidden |
| New card sort order | Order gathered | "Card type, then …" would regroup the ladder |
| Bury siblings | Off | Every card is its own note, so nothing should be buried |
| Optimize parameters | After a few hundred reviews, then about monthly | Per the Anki manual |

*Delivery:* genanki can't set these options. The alternatives are a one-time setup guide, or building the package with Anki's own Python library. It still needs checking whether Anki applies a preset from an imported package.

**Rating rubric** (printed small on the back of each card):

| Button | Recall cards | Read-through and Preview |
|---|---|---|
| Again | Got stuck, looked, used the hint, or left out a phrase | |
| Hard | All there, but with long pauses or several small slips | |
| Good | All there, with at most one small slip | |
| Easy | Instant and word-perfect | Always |

On scaffold cards (Missing words, First letters), press **Easy** whenever it felt effortless. That pushes them weeks and then months out, which is how the scaffolding retires.

**FSRS treats cards as independent.** In this deck a verse appears on six or more cards. Every review quietly strengthens that verse's other cards, and FSRS can't see that, so expect some redundant reviews. The Easy rule above is the main counterweight. In the app, this is the first thing to design differently (§9).

## 7. Output: speaking and typing

- **Default: say every recall card out loud before flipping.** Producing words aloud is a well-replicated memory booster (the "production effect"; MacLeod et al., 2010), and it costs nothing.
- **Optional type mode.** Anki card templates are HTML and JavaScript, so a card can hold a text box and buttons. Type mode would work like the Bible Memory app:
  - On Missing words, type the first letter of each missing word.
  - On Scaffolded cloze, Anchor cloze, Header → text, and Missing section, type the first letter of every hidden word.
  - Each word appears when you type its correct letter, and wrong letters flash.
  - At the end, the card shows your accuracy and the button it suggests. For example, 1 miss or fewer means Good, a few misses mean Hard, and a missed phrase means Again.

  The caveats:
  - The Anki manual provides JavaScript "without any support or warranty," and each Anki app renders cards differently. Type mode has to be tested in the Anki app on your phone.
  - The card can suggest a rating, but you still tap the button.
  - Anki's built-in "type the answer" compares the whole typed text, which is too much typing for verses on a phone.
- **Voice** isn't realistic inside Anki. It belongs to the app, and it's already listed in [ideas.md](ideas.md).

## 8. Card design

- **The map.** Outline cards show the full map: the path from the top, siblings at each level, and other branches collapsed to `▸ n`. Text cards show a compact strip: the path on one line, and the current section's parts on a second line with the current one highlighted. On a wide screen, the strip can sit beside the text.
- **Stable layout.** A unit's text is laid out the same way on every card, with small raised verse numbers. Hidden words keep their width, so the passage keeps its shape across the ladder. Readers remember where on a page they saw something (Rothkopf, 1971), and a fixed layout gives that memory something to hold.
- **Reveal in place.** The back is the front with the hidden parts revealed in the same spot, tinted, so your eyes don't hunt for the answer.
- **One prompt banner** in large type at the top, coloured by stage: outline, unit ladder, or section.
- **Rubric footer** in small type on the back, and night-mode CSS (`.nightMode`).

**Text → header**

```
front                                          back
──────────────────────────────────────         ──────────────────────────────────────
  WHERE DOES THIS BELONG?                        Doing Right by Others ›
                                                 Anger, Lust, and Remarriage ›
  ²¹ You have heard that it was said to          ANGER AND MURDER · part 1 of 2
  the ancients, ‘Do not murder’ and                         5:21–23
  ‘Anyone who murders will be subject            [map with this slot highlighted]
  to judgment.’ ²² But I tell you that …         ²¹ You have heard that it was said …
```

**Missing words** (the map strip is the same on every text card)

```
Doing Right by Others › Anger, Lust, and Remarriage
● Anger and Murder (1 of 2)   ○ Lust and Adultery   ○ Divorce and Remarriage
MISSING WORDS · 5:21–23

²¹ You ____ _____ that __ ___ said __ ___ ancients, ‘__ ___ murder’ ___
‘______ who _______ ____ be _______ __ judgment.’ ²² ___ _ tell ___ ____
anyone ___ __ angry ____ ___ brother ____ __ subject __ ________. …
```

**First letters** (░ is a soft blur in the real card; each word keeps its length)

```
FIRST LETTERS · 5:21–23

²¹ Y░░ h░░░ h░░░░ t░░░ i░ w░░ s░░░ t░ t░░ a░░░░░░░, ‘D░ n░░ m░░░░░’ a░░
‘A░░░░░ w░░ m░░░░░░ w░░░ b░ s░░░░░░ t░ j░░░░░░░.’ ²² B░░ I t░░░ y░░ t░░░
a░░░░░ w░░ i░ a░░░░ w░░░ h░░ b░░░░░░ w░░░ b░ s░░░░░░ t░ j░░░░░░░. …
```

**Missing section**

```
MISSING SECTION · The Beatitudes

³ “Blessed are the poor in spirit, for theirs is the kingdom of heaven.
⁴ Blessed are those who mourn, for they will be comforted.
⁵ Blessed are the meek, for they will inherit the earth.
┌ Triad 2 · 5:6–8 · 3 verses ───────────────────────────────────┐
│ ░░░░░░░ ░░░ ░░░░░ ░░░ ░░░░░░ ░░░ ░░░░░░ ░░░ ░░░░░░░░░░░░░, … │
└───────────────────────────────────────────────────────────────┘
⁹ Blessed are the peacemakers, for they will be called sons of God. …
```

## 9. Trial 2, and the FSRS app

**Trial 2: an unfamiliar text**
- Pick 80–120 verses you have never memorized and don't know well, with a BSB outline in `data/outlines/outlines.yml`. Use the publisher's outline as is, which is [concept.md](concept.md)'s own default. You won't know the text well enough yet to improve it.
- Tag every card with its phase and type (`phase::1`, `type::first-letters`) so the review log can be analysed by card type afterwards.
- Checkpoints:
  - When Phase 1 ends, write the outline from memory, cold.
  - On days 30, 60, and 90, recite the whole text with only the outline as a cue. Score the share of words correct in each section.
- Take notes as in trial 1. Add one number: by card type, how often you pressed Again the first time you saw a card. Anki's review log records it.

**For the FSRS app later**
- Anki's FSRS and the open-source libraries (`py-fsrs`, `ts-fsrs`, `fsrs-rs`) implement the same model. Trial 2's review log can be exported and used to fit parameters before the app exists.
- In the app, the ladder needn't be separate cards. A single memory state per unit could pick the step from how well you currently know it: First letters when recall odds are low, Header → text when they're high. That would remove the overlapping-cards problem from §6. It's an idea to test against trial 2's data, not a plan.

## 10. Decisions (made 2026-10-12)

1. **Read-through cards:** kept.
2. **Missing words pattern:** every 2nd and 3rd word hidden.
3. **Type mode:** built for Header → text only.
4. **Long recitations:** capped at about 450 words. Whole movements are practised outside the deck.
5. **Trial 1 cards:** none brought back.

Trial 2 text: **Isaiah 40–44** (BSB).

## 11. Trial 2 build

The generator is `src/deck/`. It writes to `output/isa_trial_2/`, which is git-ignored, so rebuild it to get the deck. Build and simulate:

```
venv/bin/python -m src.deck data/outlines/isaiah_40_44.yml --name "Isaiah 40–44 (trial 2)" --out output/isa_trial_2
venv/bin/python scripts/simulate_fsrs.py output/isa_trial_2
venv/bin/python -m unittest discover -s tests -t .
```

**Isaiah 40–44 at 12 new cards a day**

| | |
|---|---|
| Text | 141 verses, 3,713 words, 18 headers, 44 units of 2–6 verses |
| Cards | 436: 35 outline, 401 text |
| Days to introduce everything | 37. The outline takes days 1–5, and text starts on day 3 |
| Spacing | 41 of 44 units get a day or more between waves 1 and 2, and 42 of 44 between waves 2 and 3 |
| FSRS workload (estimate) | 24 min/day on average while new cards arrive, peaking at 35 on day 35. Then 11 min/day through day 90, and 6 after |

Most of the workload comes from volume: there are 141 Scaffolded clozes, one per verse. Read-through cards add only about 1.4 min/day.

**Where the build differs from the draft above**
- **Outline source.** BSB's book outline gives Isaiah 40–44 only 7 sections. The chapter text has its own section headings in `Chapter.json`, and those supply the next level down. Three in-text headings repeat their parent's name. They were renamed from their text (Comfort My People, I Will Help You, Sing a New Song), and `bsb_heading` keeps the original. Review those names before starting.
- **Phase 2 starts once every Phase 1 card has been *released*, not *introduced*.** Otherwise the last List the parts and Whole outline cards would be pulled forward and lose their day of spacing. All Read-throughs, Previews and Outline clozes still come before any text.
- **End of the deck.** After the last unit starts, nothing is left to fill the gaps, so the last 2–3 units get their waves on the same day.
- **Outline cloze.** The blank has a fixed width, so its length gives no hint. The map centres on the blank's parent, so the blank's own sub-headers stay collapsed: they would hint at the answer.
- **Read-through** shows the section's sub-headers inside the text, to link each header to what it labels.
- **Type mode suggestion.** Using the hint, or missing 2 or more words, suggests Again. At most one wrong letter and no missed words suggests Good. Anything else suggests Hard. A word counts as missed after 2 wrong letters, and it's then shown in red.

## Appendix: generator rules (pseudocode)

```
units = split_leaves(outline, target=80 words, max=130)    # at paragraph breaks, else verse breaks

# Phase 1: outline
for family in outline.families(breadth_first), while total headers fit the 40-header budget:
    place [ReadThrough if family is top-level] + [Preview] + [OutlineCloze(h) for each part h]
    release ListTheParts(family) +1 day
    once every family under a section with sub-sections has its ListTheParts placed:
        release WholeOutline(section) +1 day
# families past the budget: Preview, OutlineClozes, ListTheParts just before their branch's first unit

# Phase 2: text (starts after every Phase 1 card is placed)
for unit in reading order, with at most 2 units in waves 1–2 at once:
    wave1 = [TextToHeader, MissingWords, FirstLetters]
    wave2 = [ScaffoldedCloze(v) for each verse if unit has 2+ verses] + [AnchorCloze if 4+ verses]   # +1 day
    wave3 = [HeaderToText]                                                                           # +1 day
for section in post-order, once all its units' wave 3 and all its child sections have closed:
    place [MissingSection(p) for each part p of ≤ 280 words] + [FirstLines if section > 280 words]
    release SectionHeaderToText if section ≤ 450 words                                               # +1 day

# placement: "+1 day" = at least N new cards later in deck order.
# Each slot takes the oldest released card group; else the next unit/family;
# else pulls the oldest waiting group forward.
```

## References

- Bower, G. H., Clark, M. C., Lesgold, A. M., & Winzenz, D. (1969). Hierarchical retrieval schemes in recall of categorized word lists. *Journal of Verbal Learning and Verbal Behavior*, 8, 323–343.
- Glisky, E. L., Schacter, D. L., & Tulving, E. (1986). Learning and retention of computer-related vocabulary in memory-impaired patients: Method of vanishing cues. *Journal of Clinical and Experimental Neuropsychology*, 8, 292–312.
- MacLeod, C. M., Gopie, N., Hourihan, K. L., Neary, K. R., & Ozubko, J. D. (2010). The production effect: Delineation of a phenomenon. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 36, 671–685.
- Rothkopf, E. Z. (1971). Incidental memory for location of information in text. *Journal of Verbal Learning and Verbal Behavior*, 10, 608–613.
- Anki manual, Deck Options (FSRS, learning steps, display order): https://docs.ankiweb.net/deck-options.html
- FSRS algorithm (FSRS-6 default parameters): https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm
