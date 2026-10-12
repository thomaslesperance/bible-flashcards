# Bible Flashcard Generation System for use with Anki

## End goal

The least tech savvy and least talented person in my church can get set up and succeed at memorizing sections of the Bible.

## Core Concept

Separate the _content_ from the _structure_.

Terms:

- Header: A text heading dividing groups of verses. Just like h1, h2, h3 in any word processor. These are often supplied by publishers of modern translations.
- Outline: The ordered collection of headers for a given section of Scripture.

1. **Content (JSON):** A flat dictionary of raw Bible verses (e.g., `"Matt 5:3": "Blessed are the..."`).<br>
   Text-key heirarchy, most to least atomic, with example value:<br>
   `"testament": "new"`<br>
   `"book": "matthew"`<br>
   `"chapter": "4"`<br>
   `"verse": "10"`<br>

   A `"part": "a"` also seems necessary to allow references like 'Matthew 4:12a' which would be especially useful for poetry. But since this would likely need to be manually added on an as-needed basis, I am not sure if this better belongs in the YAML file.<br>

2. **Structure (YAML):** A hierarchical outline mapping text headers to verse references.<br>
   Heirarchy of headers from most to least atomic:<br>
   `verse`<br>
   `chapter`<br>
   `book`<br>
   `testament`<br>
   `h_<n>` (where n is heirarchy depth) <br>
   `h_<n-1>` (where n is heirarchy depth) <br>
   `h_<n-2>` (where n is heirarchy depth) <br>
   `...`
3. **Compiler (Python):** A script that marries the two, applying a consistent algorithmic schema to automatically generate progressive Anki flashcards (CSVs) at varying difficulties.<br><br>

**Note**: This all implies that whatever outline is chosen will become cemented in the user's memory by being the skeleton on which the verses are attached. On one hand, this creates a lot of pressue to identify the most biblically accurate outline for whatever section of the Bible you're working on. Since the headers available in modern translations are supplied by the publisher, and chapter divisions are supplied by medeival sources, and neither are defensible in their arrangement on many occasions.

But on the other hand, perhaps it's not _that_ big of a deal. While it would be nice to start from the perfect outline for every passage, to do so would require totally clear understanding, which usually never comes without much time spent meditating, dwelling, reading, and re-reading. Which is precisely the activity this project intends to facilitate and improve.

Therefore, it seems in order to supply the user with the default outline constituted by the headers provided by the publisher of whatever translation is being drawn from. And then, if the user has heard from the Lord and received insight into the meaning of a passage that corrects and thereby diverges from the publisher's outline, he or she may supply that corrected outline in the YAML file and resume internalizing the passage in that manner. This way, working on one's memory of the Bible is not hindered by the clarity of understanding necessary to 'rightly divide the text', since the former enables the latter.

## Graduated Difficulty

Each deck will follow a system of graduated difficulty. In the Biblical Hebrew deck I am using to memorize 600+ vocabulary works, the deck is ordered by number of occurances in the Hebrew Bible.

For this project, the cards would need to be ordered, collected into subdecks, or configured in Anki in such a way that the easiest cards are worked through first, gradually building the user to recalling larger and larger pieces of text at once.

At this point, I am not sure if there needs to be different subdecks for differing levels of difficulty, or if all the cards should be in one deck and simply ordered by difficulty.

I am also not 100% confident yet on the following progressive difficulty system, since this will need to be applied to a group of verses of any size (e.g., the entire book of Luke versus Romans 8:1-12)

### Level 1

Recall a missing outline header within a section of the outline.

- Anchored and scaffolded (see below) for wide sections of outline
- Scaffolded for narrow sections (even 2 units long) of outline
- Progresses in difficulty from smallest to largest outline section

### Level 2

Recall header from text (one sibling of reversible card, see below)

- Progresses in difficulty from smallest to largest outline section

### Level 3

Recall a single missing verse within a section of verses.

- Anchored and scaffolded (see below)
- Progresses in difficulty from smallest to largest outline section
- But there should be more clozes the larger the outline section becomes
- But there should be a limit to the size of this, or it will become unwieldy, perhaps even limit this level to only the outline "leaves" (smallest units, like paragraphs or h_n)

### Level 4

Recall an entire section of text missing from a larger section of text.<br>
And, recall an entire section of text indicated by a missing header in a section of outline.

### Level 5

Recall text given an outline header.
Outward-in, ending in recall of entire text.

### Thoughts

- Long learning phase to prevent "ease hell"
- Somehow broaden scope enough to prevent grinding on 1 or 2 paragraphs as you move through the text
- e.g., if max_scope = 30 paragraphs, then moving through Romans would have you working on all paragraphs in Romans 1-3 simultaneously

## Card Schemas & Algorithms

Code needs to correspond directly to how hard it is to sit down and memorize a unit of text.
What is the largest number of verses that can be memorized by the average person at once? Probably a single verse. Therefore, the logic flow would look something like:

```
use_scaffolding = false
use_anchoring = false

framework = <hierarchy of headings containing verses>

for unit in framework:
  if len(unit) > 1:
    use_scaffolding = true

  if len(unit) > 2:
    use_anchoring = true

  ... other tests for other card types ...

  scaffolded_rows = scaffold_unit(unit)
  anchored_rows = anchor_unit(unit)

  ... other functions for other card types ...

```

Card schemas need to leverage learning science to the greatest extent possible to maximize effectiveness and time efficiency when working through the cards. Some ideas are as follows:

### 1. Progressive Overload (The Baseline)

- **Trigger:** Any atomic grouping (> 1 verses).
- **Science:** _Scaffolding & Desirable Difficulty_. You need high context initially to build the memory trace, then remove it to test true recall.
- **Algorithm:** Generate 2 card types.
  - _Scaffolded:_ `{{c1::v1}} {{c2::v2}} {{c3::v3}}` (Tests 1 verse, uses the others as hints).

### 2. The Anchor Schema (Contextual Bridging)

- **Trigger:** `if len(verses) > 3 and is_paragraph`:
- **Science:** _Serial Position Effect_. We naturally remember the first (primacy) and last (recency) items in a sequence, but forget the middle. Anchors provide the necessary entry/exit nodes to retrieve the middle block.
- **Algorithm:** Leave the first and last verse visible; cloze the middle.
  - `v1 (visible) {{c1::v2}} {{c1::v3}} v4 (visible)`

### 3. First-Letter Prompting (Interference Mitigation)

- **Trigger:** `if is_list` (e.g., genealogies or highly repetitive texts like Beatitudes) OR `if len(verses) > 5`:
- (Not 100% on the exact trigger, but I do want to include this. Things like the list of the 12 apostles or the table of nations might benefit from this. I know there's a popular Bible memory app that seems to major on this method. It might be purdent to investigate how they use it across text forms. If it is desired, it might be configured in the YAML file.)
- **Science:** _Cue-Dependent Forgetting_. When texts are too similar, they interfere with each other. A minimal cue (first letter) bypasses the interference without giving away the answer.
- **Algorithm:** Convert text to initials for the cloze.
  - `{{c1::J::James,}} {{c1::P::Peter,}} {{c1::John::John,}} {{c1::T::Thomas,}}...`

### 4. Bidirectional Concept Retrieval

- **Trigger:** Any named outline header.
- **Science:** _Associative Memory_. Being able to recite text is only half the battle; you must be able to retrieve the text when prompted by a concept, and identify the concept when reading the text.
- **Algorithm:** Generate Basic (Reversible) cards mapping the Header to the block of text.
  - _Forward:_ `Header -> Text` (Recall text given outline).
  - _Reverse:_ `Text -> Header` (Identify context given text).

## Practical Deployment & Distribution

### 1. Copyright & Translation Licenses

Most modern translations (ESV, NIV, NKJV, NASB) are **copyrighted**. While personal use or small church group distribution often falls under fair use or generous publisher allowances (e.g., up to 500 verses), seems I cannot legally distribute a comprehensive Anki deck of a copyrighted translation on the open internet. For public, wide-scale sharing, I may be limited to a public domain text like the World English Bible (WEB) or King James Version (KJV).

### 3. Controlling Anki Deck Settings

1. Need to determine the best Anki settings for cards generated by this project.
2. Need to determine exactly how to enforce those settings to eliminate all Anki configuration for end user if possible.

# Brainstorm

Phase 1:

- Easily produce a deck for any section of Scripture
- Produce a few decks for myself, such as Epistles, SOM, Farewell Discourse, Revelation, Isaiah, Psalms
- All decks use HTML/CSS template
- Include helpful info in extra info fields, such as chapter, verse, book, etc.
- Custom color or theme on top of template for each deck (e.g., red for Romans)
- Create logins for friends and sync decks to their account on my laptop so they just need to login in browser
- Collect user feedback on effectiveness of card schemas and UX suggestions for possible phase 2 mobile app

Phase 2: React Native iOS and Android app:

- Built on open-source Anki?
- Some way to navigate licensing for translations
  - how does BLB or BibleGateway do it?
- Beautiful UI
- User accounts
- Groups that church members can create to share custom decks or outlines
- Simplified UI controlling complicated Anki settings under the hood
- Beautiful, unique HTML/Bootstrap theme for each deck
- Build the app I would want to use and then worry about licensing later?
- Imagine end goal and work backward

## Project Needs

- Solid research and most effective techniques for memorizing text
- Solid, concise teaching on benefits and purpose of internalizing Scripture to inform, motivate, and guide users
- Well-chosen default framework
- Visually appealing and fun interface/schtick (for the mobile app)
  - Framework is the branches
  - Verses are the leaves
  - As you go through the book or section, you fill out the branch
  - You have a visual global map of the whole Bible that shows the parts you've completed

## TODO

1. Download Bible in JSON, enrich with heirarchy as needed
2. Iron out difficulty levels that will adapt to any text size for the best UX (read more on any other useful card type)
3. Iron out how cards need to be ordered, tagged, supplied with meta data, etc., to accomplish 2
4. Iron out pseudo for algorithm for implementing 3 given any given outline (placeholders for helpers)
5. Implement draft of module that implements 4 (placeholders for helpers)
6. Implement draft of module that implements all helpers called by 5
7. Test run on Sermon on the Mount
