# Free Use Bible API docs, and what they changed in src

Findings from reading https://bible.helloao.org/docs/ and checking them against `data/bible.eng.db`. The second half covers the code written as a result: `src/chapter.py` and a change to `src/books.py`. Written 2026-10-12.

## Summary

- **The docs describe our database.** `bible.eng.db` is the English download of the Free Use Bible API. Its JSON columns (`Chapter.json`, `ChapterVerse.contentJson`) hold exactly the objects the API's TypeScript interfaces describe. `data/bible.eng.yml` lists the columns. The docs are the only place the JSON inside them is described.
- **Verified, not assumed.** `src/chapter.py` parses `Chapter.json` into typed objects. Across all 31,086 BSB verses, its text matches the DB's plain `ChapterVerse.text` with 0 mismatches.
- **For trial 2, the important part is poetry layout.** BSB Isaiah is poetry. Each line comes with an indent level, which the card templates need to keep the text's shape (sequence v2, §8).
- **Word-level data (Strong's numbers, lemmas) doesn't apply to BSB.** BSB has none, so cards tokenize words themselves.
- **The SDK is a TypeScript HTTP client, not an ORM.** The TypeScript types still matter for a React Native app. The Python generator and the app can share one JSON card format, so the generator doesn't have to move to TypeScript.

## 1. What the site offers

| Area | Contents | Endpoint pattern (base `https://bible.helloao.org`) |
|---|---|---|
| Translations | 1,256 translations, 1,004 languages. Headings, poetry indents, footnotes, words-of-Jesus flags, audio links and timings, word-level annotations | `/api/available_translations.json`, `/api/{translation}/books.json`, `/api/{translation}/{book}/{chapter}.json`, `…/{chapter}.words.json`, `…/{chapter}.{reader}.audioTimings.json`, `/api/{translation}/complete.json` |
| Datasets | Cross-references with a relevance `score`. People, places, events and people groups, each linked to verses | `/api/d/{dataset}/{book}/{chapter}.json`, `/api/d/{dataset}/people.json` (and `places`, `events`, `groups`) |
| Commentaries | Adam Clarke; Tyndale Open Study Notes (with 125 topic "profiles", e.g. `aaron`) | `/api/c/{commentary}/{book}/{chapter}.json`, `/api/c/{commentary}/profiles.json` |
| Downloads | `bible.db` (11 GB, all languages), `bible.eng.db` (1.5 GB, English, the one in `data/`), `api.zip` (1.5 GB, the static API) | `/docs/guide/downloads.html` |
| SDK | npm `free-use-bible-api`: a TypeScript client over `fetch`, with in-memory caching and helpers (`getVerseText`, `getNextChapter`) | `/docs/sdks/javascript.html` |

- **Licensing.** The API is MIT licensed. There's no key, no sign-up and no stated rate limit, and storing, caching and offline copies are allowed. Each translation keeps its own license notice (`licenseNotice` in the DB), and an app must show it.
- **No Python SDK.** The only SDK is JavaScript/TypeScript.
- **The SDK isn't offline-first.** Its cache is in memory only. The docs don't say whether it runs in React Native.
- **No download schema.** The Downloads page doesn't document the SQLite schema. `data/bible.eng.yml` fills that gap.

## 2. Which interfaces match which tables

| TypeScript interface (docs) | Where it lives in `bible.eng.db` |
|---|---|
| `Translation` | `Translation` table, also copied onto every row of the other tables |
| `TranslationBook` | `Book` table. `id` is a USFM code (`ISA`, `MAT`) |
| `ChapterData` (`number`, `content[]`, `footnotes[]`) | `Chapter.json` |
| `ChapterVerse.content` | `ChapterVerse.contentJson`. `ChapterVerse.text` is the same verse as plain text |
| `ChapterFootnote` | `ChapterFootnote` table, and inside `Chapter.json` |
| `ChapterWord` | `ChapterWords.wordsJson` |
| `TranslationBookChapterAudioLinks` | `ChapterAudioUrl` (8,323 rows) |
| `TranslationBookChapterAudioTimings` | `ChapterAudioTiming`: **0 rows locally**. Read-along timings would have to come from the API |
| `DatasetReference` | `DatasetReference` (344,799 rows, with `score`) |
| Commentary types | `Commentary`, `CommentaryBook`, `CommentaryChapter`, `CommentaryChapterVerse` |

The `id:1`, `name:1` and `sha256:1` columns in the yml are real. `PRAGMA table_info` shows them on the tables themselves: the download denormalizes the translation's metadata onto every row.

### The chapter content model

```
ChapterData
  content: (heading | line_break | verse | hebrew_subtitle)[]
    heading           { type, content: string[] }               a section heading
    line_break        { type }                                  a paragraph break between verses
    hebrew_subtitle   { type, content: [...] }                  a psalm superscription
    verse             { type, number, content: [...] }
      content items:  string                                    prose
                      { text, poem?, wordsOfJesus? }            poem = indent level of a poetry line
                      { lineBreak: true }                       a line break inside the verse
                      { heading }                               a heading inside the verse
                      { noteId }                                a footnote marker
  footnotes: { noteId, text, caller, reference?: {chapter, verse} }[]
```

## 3. What BSB actually contains

From a scan of all 1,189 BSB chapters:

| Shape | Count | Note |
|---|---:|---|
| `verse` | 31,086 | |
| `line_break` (paragraph break) | 13,894 | Where §4 of sequence v2 splits long leaves |
| `heading` | 3,091 | BSB's own section headings |
| `hebrew_subtitle` | 116 | Psalm titles |
| Poetry line `{text, poem}` | 24,507 | Indent levels 1 and 2 |
| Plain prose string | 27,944 | |
| Footnote marker `{noteId}` | 4,817 | Must be stripped from card text |
| `{lineBreak}` inside a verse | 3,636 | |
| `{heading}` inside a verse | **0** | |
| `wordsOfJesus` | **0** | BSB has no red-letter data |
| `{text, descriptive: true}` | 1 | Zech 12:1. **Not in the API docs** |

- **Word-level data.** `ChapterWords` has rows for 25 of the 51 English translations, and **none for BSB**.
- **Isaiah 40 sample.** It has 31 verses, 9 paragraph breaks and 3 headings. Most verses are pairs of poetry lines at indents 1 and 2. A few mix in prose, e.g. 40:3 opens "A voice of one calling:" before the poetry.

## 4. What was built in src

### `src/books.py`

- **New field.** `Book` has a `usfm` field (`"ISA"`, `"MAT"`), and there's a new `BY_USFM` lookup. The DB and the API use USFM codes. Our refs use OSIS IDs (`Isa`, `Matt`), and nothing mapped between them before.
- **Ordering check.** The codes are listed in canonical order next to `_RAW`, and an `assert` checks the two lists are the same length. The list matches BSB's 66 `Book.id` values in order.

### `src/chapter.py`

Two layers.

**1. Raw layer: TypedDicts that mirror the TypeScript interfaces field-for-field.**
- Classes: `ChapterData`, `ChapterVerse`, `ChapterHeading`, `ChapterLineBreak`, `ChapterHebrewSubtitle`, `FormattedText`, `InlineHeading`, `InlineLineBreak`, `VerseFootnoteReference`, `ChapterFootnote`, `ChapterWord`.
- The names match the docs so that the Python generator and a future TypeScript app use the same vocabulary.
- `FormattedText` also has the undocumented `descriptive` flag.

**2. Card layer: frozen dataclasses for the card generator.**

```
Chapter(ref, translation, blocks, footnotes)
  blocks: Heading | Subtitle | ParagraphBreak | Verse
  Verse(ref: VerseRef, lines: tuple[Line], note_ids)
    .text, .word_count
    Line(text, indent)          indent = poetry level, 0 for prose
      .words -> [Word(text, start, end)]   offsets into Line.text
```

Entry points:
- `load_chapter(translation, osis_book, chapter)` reads `Chapter.json` through `src/db.py` (`fetch_one`). Example: `load_chapter("BSB", "Isa", 40)`.
- `parse_chapter(data, osis_book, translation)` does the same flattening on a `ChapterData` dict already in memory.

Design choices:
- **Lines, not run-on text.** Each poetry item becomes its own `Line` with its indent. Consecutive prose pieces are joined into one line, and a `{lineBreak}` ends the current line. Cards can then lay a passage out identically on every card (sequence v2, §8).
- **Word offsets, like `ChapterWord.start/end`.** Missing words and First letters can blank or blur just a word's characters. Quotes, commas and dashes stay visible, so each blank keeps its word's width. A word is letters/digits with inner apostrophes or hyphens (`LORD’s`, `well-being`), matched by `\w(?:[\w’'-]*\w)?`.
- **Footnotes are kept apart.** Markers are removed from the text. Their ids stay on `Verse.note_ids`, and their text in `Chapter.footnotes`.
- **Unknown shapes fail loudly.** An inline heading raises `ValueError`. BSB has none to test against, so the parser doesn't guess where it goes.
- **`wordsOfJesus` is dropped from the card layer.** BSB has no such data. Other translations still have it in the raw layer.

### Validation

A one-off script (not committed) parsed every BSB chapter and compared each `Verse.text` with `ChapterVerse.text`, ignoring whitespace:

| Check | Result |
|---|---|
| Verses parsed | 31,086 (matches the `ChapterVerse` row count) |
| Text mismatches | 0 |
| A verse number appearing twice in one chapter | 0 |
| Isaiah 40–44, BSB | 141 verses, 3,713 words (about 26 words per verse) |

Isaiah 40:1–2 as the loader returns it:

```
     Heading(text='Prepare the Way for the LORD')
  1 (7 words)
          “Comfort, comfort My people,”
              says your God.
  2 (35 words)
          “Speak tenderly to Jerusalem,
              and proclaim to her
          that her forced labor has been completed;
              her iniquity has been pardoned.
          For she has received from the hand of the LORD
              double for all her sins.”
     ParagraphBreak()
```

## 5. How this serves sequence v2

| Sequence v2 need | Provided by |
|---|---|
| Split long leaves at paragraph breaks, sized in words (§4) | `ParagraphBreak` blocks, `Verse.word_count` |
| Stable layout across the ladder (§8) | `Line.indent`, with one line per poetry line |
| Missing words: every 2nd and 3rd word blanked, each blank as wide as its word | `Line.words` offsets |
| First letters, blurred in place | `Word.text[0]` and offsets |
| Type mode on Header → text (first letters) | `Line.words` gives the expected letter sequence |
| Map strip and headers | The outline comes from `data/outlines/outlines.yml`. `Heading` blocks can cross-check it |
| Dimmed neighbour verses (Scaffolded cloze) | `Chapter.verses` in order |

## 6. The TypeScript and React Native question

- **Card format.** An app written in TypeScript doesn't require the generator to be. The two meet at a card format: JSON written by the Python generator, read by the app. The app can import the API's types from the `free-use-bible-api` package or copy them into its own `types.ts`. That's why the raw layer in `chapter.py` keeps the TypeScript names.
- **FSRS.** `py-fsrs` and `ts-fsrs` implement the same FSRS model, so trial 2's simulator can run in Python now and the app can schedule with `ts-fsrs` later.
- **Offline text.** The SDK only caches in memory. For offline use, the app would bundle a trimmed SQLite of the one or two translations it needs, or the generated card JSON itself.
- **Datasets for later features.** Cross-references (`DatasetReference.score`, to keep the top N per verse), people/places/events, and Tyndale profiles are the API's main extras beyond the text.

## 7. Open items

- **`split_units()`** (§4: 80-word target, 130-word maximum, split at paragraph breaks) is the next piece. Running it on Isaiah 40–44 will give trial 2's real unit and card counts.
- **Trial 2 runs longer than planned.** Isaiah 40–44 is 141 verses, against the draft's 80–120. The Sermon on the Mount's 30-day plan will stretch.
- **Two text loaders.** `src/bible.py` still loads its own JSON-file format. Once the generator is built, `Bible` could be built from `load_chapter` so there's one source of text.
- **No tests yet.** The validation above was a one-off script. A test that compares `Verse.text` with `ChapterVerse.text` for a few chapters would protect the parser.
- **Attribution.** Any app built on this data must show each translation's `licenseNotice`.
