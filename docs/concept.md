# The Anki Bible Compilation System

**Core Concept:** Separate the _content_ from the _structure_.

1. **Content (JSON):** A flat dictionary of raw Bible verses (e.g., `"Matt 5:3": "Blessed are the..."`).
2. **Structure (YAML):** A hierarchical outline mapping headers to verse references.
3. **Compiler (Python):** A script that marries the two, applying a consistent algorithmic schema to automatically generate progressive Anki flashcards (CSVs) at varying difficulties.

---

## Learning-Science Card Schemas & Algorithms

To build a cohesive, algorithmic system, define your atomicity levels (e.g., `LEVELS = [Verse, Paragraph, Section, Chapter]`) and apply these schemas based on the node's properties:

### 1. Progressive Overload (The Baseline)

- **Trigger:** Any atomic grouping (1-3 verses).
- **Science:** _Scaffolding & Desirable Difficulty_. You need high context initially to build the memory trace, then remove it to test true recall.
- **Algorithm:** Generate 2 card types.
  - _Scaffolded:_ `{{c1::v1}} {{c2::v2}} {{c3::v3}}` (Tests 1 verse, uses the others as hints).
  - _Unscaffolded:_ `{{c1::v1}} {{c1::v2}} {{c1::v3}}` (Tests all verses simultaneously).

### 2. The Anchor Schema (Contextual Bridging)

- **Trigger:** `if len(verses) > 3 and is_paragraph`:
- **Science:** _Serial Position Effect_. We naturally remember the first (primacy) and last (recency) items in a sequence, but forget the middle. Anchors provide the necessary entry/exit nodes to retrieve the middle block.
- **Algorithm:** Leave the first and last verse visible; cloze the middle.
  - `v1 (visible) {{c1::v2}} {{c1::v3}} v4 (visible)`

### 3. First-Letter Prompting (Interference Mitigation)

- **Trigger:** `if text_similarity_is_high` (e.g., genealogies or highly repetitive texts like Beatitudes) OR `if len(verses) > 5`:
- **Science:** _Cue-Dependent Forgetting_. When texts are too similar, they interfere with each other. A minimal cue (first letter) bypasses the interference without giving away the answer.
- **Algorithm:** Convert text to initials for the cloze.
  - `{{c1::B::Blessed}} {{c1::a::are}} {{c1::t::the}} {{c1::p::poor}}...`

### 4. Bidirectional Concept Retrieval

- **Trigger:** Any named outline header.
- **Science:** _Associative Memory_. Being able to recite text is only half the battle; you must be able to retrieve the text when prompted by a concept, and identify the concept when reading the text.
- **Algorithm:** Generate Basic (Reversible) cards mapping the Header to the block of text.
  - _Forward:_ `Header -> Text` (Recall text given outline).
  - _Reverse:_ `Text -> Header` (Identify context given text).

---

## Practical Deployment & Distribution

### 1. Copyright & Translation Licenses

If you plan to distribute your decks, remember that most modern translations (ESV, NIV, NKJV, NASB) are **copyrighted**. While personal use or small church group distribution often falls under fair use or generous publisher allowances (e.g., up to 500 verses), you cannot legally distribute a comprehensive Anki deck of a copyrighted translation on the open internet. For public, wide-scale sharing, use a public domain text like the World English Bible (WEB) or King James Version (KJV).

### 2. Training Non-Tech Savvy Users

The architectural complexity (Python, YAML, CSVs) is for the **deck creator only**. To distribute this to non-tech savvy users, the workflow is incredibly simple:

1. **You** generate the cards, import them into your Anki, and organize the subdecks.
2. **You** export the finished product from Anki as an Anki Package (`.apkg` file).
3. **The User** simply downloads the Anki app (mobile or desktop), double-clicks your `.apkg` file to import it, and hits "Study Now." They never see the code or the CSVs.

### 3. Preserving Anki Deck Settings

Scripture memorization requires different pacing than standard vocabulary flashcards (you usually need more repetition in the early stages).

- **How to preserve settings:** You do not need to teach users how to configure Anki! Create a specific Deck Options Group in your Anki (e.g., "Bible Memorization"), assign it to your master deck, and configure your preferred intervals. When you export the `.apkg`, **Anki automatically packages those exact deck settings into the file** and applies them to the user's app when imported.
- **Recommended Settings:** Increase `Learning steps` to something like `1m 10m 1d 3d` so users see the verses more frequently in the early stages before the intervals grow too large.

# Brainstorm

- Built on open-source Anki?
- Some way to navigate licensing for translations
- how does BLB or BibleGateway do it?
- React Native iOS and Android app
- Beautiful UI
- User accounts
- Groups users can join for churches
- Shared sets of material to memorize within groups
- Simplified UI controlling Anki settings under the hood
- Beautiful, unique HTML/Bootstrap theme for each deck
- Build the app I would want to use
- And then worry about licensing later?
- Imagine end goal and work backward
- Might just have the default outline be the headings from whatever Bible translation
- And then you can import your own outline based on study or whatever special section or grouping (even non-contiguous)

## End goal

The least tech savvy and the least talented person in my church can get set up and succeed at memorizing sections of the Bible.

## Algorithm

Code needs to correspond directly to how hard it is to sit down and memorize a verse.
What is the largest # of verses that can be memorized at once? Probably a single verse. Therefore:

```
for unit in framework:
  if len(unit) > 1:
    use_scaffolding = true
    use_anchoring = true
```

## In-practice

Each deck will follow the same gradual difficulty of subdecks based on the algorithm above.

### Level 1 (Subdeck 1)

Cloze deletion of the outline headers.

### Level 2 (Subdeck 2)

Cloze deletion of text within the outline headers (scaffolded and anchored).
Recall outline header given a text unit for all groupings.

### Level 3 (Subdeck 3)

Recall text given an outline header.
Work on the smallest subdecks first, one at a time.
Gradually move to the larger groupings.

### Level 4

Recite the whole text.
