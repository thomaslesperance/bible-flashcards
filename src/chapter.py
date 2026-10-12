"""
Chapter text from data/bible.eng.db (the Free Use Bible API's SQLite download).

Chapter.json holds a ChapterData object. The TypedDicts below mirror the API's
TypeScript interfaces field-for-field, so the app can use the same names:
https://bible.helloao.org/docs/reference/translations/standard.html

load_chapter() flattens one into what cards need: headings, paragraph breaks,
and verses as lines (with their poetry indent) whose words carry character
offsets, so a card can blank or blur a word in place without reflowing the text.
"""

import json
import re
from dataclasses import dataclass
from typing import Literal, NotRequired, TypedDict

from .books import BY_OSIS
from .db import fetch_one
from .refs import VerseRef


# Raw JSON, as stored in Chapter.json ----------------------

class FormattedText(TypedDict):
    text: str
    poem: NotRequired[int]  # indent level of a poetry line
    wordsOfJesus: NotRequired[bool]
    descriptive: NotRequired[bool]  # not in the API docs; seen once in BSB (Zech 12:1)


class InlineHeading(TypedDict):
    heading: str


class InlineLineBreak(TypedDict):
    lineBreak: Literal[True]


class VerseFootnoteReference(TypedDict):
    noteId: int


type VerseContent = str | FormattedText | InlineHeading | InlineLineBreak | VerseFootnoteReference


class ChapterHeading(TypedDict):
    type: Literal["heading"]
    content: list[str]


class ChapterLineBreak(TypedDict):
    type: Literal["line_break"]


class ChapterHebrewSubtitle(TypedDict):
    type: Literal["hebrew_subtitle"]
    content: list[str | FormattedText | VerseFootnoteReference]


class ChapterVerse(TypedDict):
    type: Literal["verse"]
    number: int
    content: list[VerseContent]


type ChapterContent = ChapterHeading | ChapterLineBreak | ChapterVerse | ChapterHebrewSubtitle


class FootnoteReference(TypedDict):
    chapter: int
    verse: int


class ChapterFootnote(TypedDict):
    noteId: int
    text: str
    reference: NotRequired[FootnoteReference]
    caller: str | None


class ChapterData(TypedDict):
    number: int
    content: list[ChapterContent]
    footnotes: list[ChapterFootnote]


class ChapterWord(TypedDict):
    """One entry of ChapterWords.wordsJson. Only some translations have these; BSB doesn't."""
    contentIndex: int
    start: int
    end: int
    strongs: NotRequired[list[str]]
    lemma: NotRequired[str]
    morph: NotRequired[str]
    srcloc: NotRequired[str]
    occurrence: NotRequired[int]
    occurrences: NotRequired[int]


# Flattened model for card generation ----------------------

# A word is letters/digits, with inner apostrophes or hyphens ("LORD’s", "well-being").
# Quotes, commas and dashes stay outside it, so they remain visible on a blanked card.
_WORD_RE = re.compile(r"\w(?:[\w’'-]*\w)?")


@dataclass(frozen=True)
class Word:
    text: str
    start: int  # offsets into Line.text, like ChapterWord.start/end
    end: int


@dataclass(frozen=True)
class Line:
    text: str
    indent: int  # poetry indent level; 0 for prose

    @property
    def words(self) -> list[Word]:
        return [Word(m[0], m.start(), m.end()) for m in _WORD_RE.finditer(self.text)]


@dataclass(frozen=True)
class Verse:
    ref: VerseRef
    lines: tuple[Line, ...]
    note_ids: tuple[int, ...]  # footnotes attached to this verse (markers are stripped from the text)

    @property
    def text(self) -> str:
        return " ".join(line.text for line in self.lines)

    @property
    def word_count(self) -> int:
        return sum(len(line.words) for line in self.lines)


@dataclass(frozen=True)
class Heading:
    text: str


@dataclass(frozen=True)
class Subtitle:
    """A psalm superscription ("Of David."), which sits before verse 1."""
    text: str


@dataclass(frozen=True)
class ParagraphBreak:
    pass


type Block = Heading | Subtitle | ParagraphBreak | Verse


@dataclass(frozen=True)
class Chapter:
    ref: VerseRef  # verse is None
    translation: str
    blocks: tuple[Block, ...]
    footnotes: dict[int, str]  # noteId -> text

    @property
    def verses(self) -> list[Verse]:
        return [b for b in self.blocks if isinstance(b, Verse)]

    def verse(self, number: int) -> Verse:
        for v in self.verses:
            if v.ref.verse == number:
                return v
        raise KeyError(f"{self.ref}:{number} is not in {self.translation}")


def _flatten_verse(ref: VerseRef, content: list[VerseContent]) -> Verse:
    lines: list[Line] = []
    prose: list[str] = []  # prose pieces waiting to be joined into one line
    note_ids: list[int] = []

    def end_prose():
        if prose:
            lines.append(Line(" ".join(prose), 0))
            prose.clear()

    for part in content:
        if isinstance(part, str):
            prose.append(part)
        elif "text" in part:
            if "poem" in part:
                end_prose()
                lines.append(Line(part["text"], part["poem"]))
            else:
                prose.append(part["text"])
        elif "lineBreak" in part:
            end_prose()
        elif "noteId" in part:
            note_ids.append(part["noteId"])
        else:
            # InlineHeading: none in BSB, so there's no tested way to place it yet.
            raise ValueError(f"Unhandled verse content in {ref}: {part!r}")
    end_prose()
    return Verse(ref, tuple(lines), tuple(note_ids))


def _plain(content: list) -> str:
    """Text of heading/subtitle content, without footnote markers."""
    return " ".join(p if isinstance(p, str) else p["text"] for p in content
                    if isinstance(p, str) or "text" in p)


def parse_chapter(data: ChapterData, book: str, translation: str) -> Chapter:
    """Flatten a ChapterData object. `book` is an OSIS ID."""
    blocks: list[Block] = []
    for c in data["content"]:
        if c["type"] == "verse":
            blocks.append(_flatten_verse(VerseRef(book, data["number"], c["number"]), c["content"]))
        elif c["type"] == "heading":
            blocks.append(Heading(" ".join(c["content"])))
        elif c["type"] == "hebrew_subtitle":
            blocks.append(Subtitle(_plain(c["content"])))
        elif c["type"] == "line_break":
            blocks.append(ParagraphBreak())
        else:
            raise ValueError(f"Unhandled chapter content in {book} {data['number']}: {c!r}")
    footnotes = {f["noteId"]: f["text"] for f in data["footnotes"]}
    return Chapter(VerseRef(book, data["number"]), translation, tuple(blocks), footnotes)


def load_chapter(translation: str, book: str, chapter: int) -> Chapter:
    """Load one chapter from bible.eng.db. `book` is an OSIS ID, e.g. load_chapter("BSB", "Isa", 40)."""
    row = fetch_one(
        "SELECT json FROM Chapter WHERE translationId = ? AND bookId = ? AND number = ?",
        (translation, BY_OSIS[book].usfm, chapter),
    )
    if row is None:
        raise KeyError(f"{VerseRef(book, chapter)} is not in {translation}")
    return parse_chapter(json.loads(row["json"]), book, translation)
