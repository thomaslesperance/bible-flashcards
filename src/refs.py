"""
Parsing for human-written Bible references.

Supported forms (book names are flexible, see books.lookup_book):
    Matt 5            whole chapter
    Matt 5-7          chapter range
    Matt 5:3          single verse
    Matt 5:3a         part of a verse (parts are defined by `splits` in an outline)
    Matt 5:3-12       verse range
    Matt 5:48-6:4     range crossing a chapter boundary
    Matt 6:9b-13      ranges may start/end on a part
    Jude 3            single-chapter books take a bare verse number
"""

import re
from dataclasses import dataclass

from .books import BY_OSIS, SINGLE_CHAPTER, lookup_book


@dataclass(frozen=True)
class VerseRef:
    book: str  # OSIS ID
    chapter: int
    verse: int | None = None  # None = whole chapter (only inside a Passage)
    part: str | None = None  # "a", "b", ...

    @property
    def key(self) -> str:
        """Canonical key used in Bible JSON files, e.g. 'Matt.5.3' (parts are not part of the key)."""
        return f"{self.book}.{self.chapter}.{self.verse}"

    @property
    def sort_key(self) -> tuple:
        return (BY_OSIS[self.book].index, self.chapter, self.verse or 0, self.part or "")

    def whole(self) -> "VerseRef":
        return VerseRef(self.book, self.chapter, self.verse)

    def __str__(self) -> str:
        name = BY_OSIS[self.book].name
        if self.verse is None:
            return f"{name} {self.chapter}"
        return f"{name} {self.chapter}:{self.verse}{self.part or ''}"


@dataclass(frozen=True)
class Passage:
    start: VerseRef
    end: VerseRef

    @property
    def is_single_verse(self) -> bool:
        return self.start == self.end and self.start.verse is not None


_REF_RE = re.compile(r"^\s*(?P<book>(?:[1-3]\s*)?[^\d\s][^\d]*?)\s*(?P<rest>\d.*?)\s*$")
_POINT_RE = re.compile(r"^(?P<a>\d+)(?::(?P<b>\d+)(?P<part>[a-z])?)?(?P<bare_part>[a-z])?$")


def _parse_point(text: str, book: str, default_chapter: int | None, single_chapter: bool) -> VerseRef:
    m = _POINT_RE.match(text)
    if not m:
        raise ValueError(f"Can't parse {text!r}")
    a, b = int(m["a"]), m["b"]
    if b is not None:
        return VerseRef(book, a, int(b), m["part"])
    # A bare number: a verse if we're already inside a chapter, else a chapter.
    if default_chapter is not None:
        return VerseRef(book, default_chapter, a, m["bare_part"])
    if single_chapter:
        return VerseRef(book, 1, a, m["bare_part"])
    if m["bare_part"]:
        raise ValueError(f"A part letter needs a verse, not a chapter: {text!r}")
    return VerseRef(book, a)


def parse_passage(text: str) -> Passage:
    """Parse a reference or range into a Passage. Raises ValueError with a readable message."""
    m = _REF_RE.match(text)
    if not m:
        raise ValueError(f"Can't parse reference {text!r}")
    try:
        book = lookup_book(m["book"])
    except ValueError as e:
        raise ValueError(f"{e} in reference {text!r}") from None
    single = book.osis in SINGLE_CHAPTER
    rest = m["rest"].replace(" ", "").replace("–", "-").replace("—", "-")

    try:
        if "-" in rest:
            left, right = rest.split("-", 1)
            start = _parse_point(left, book.osis, None, single)
            # "5:3-12" -> 12 is a verse in chapter 5; "5-7" -> 7 is a chapter
            end = _parse_point(right, book.osis, start.chapter if start.verse is not None else None, single)
        else:
            start = end = _parse_point(rest, book.osis, None, single)
    except ValueError as e:
        raise ValueError(f"{e} in reference {text!r}") from None

    if (start.verse is None) != (end.verse is None):
        raise ValueError(f"Mixed chapter/verse range in {text!r}")
    if end.sort_key < start.sort_key:
        raise ValueError(f"Range runs backwards in {text!r}")
    return Passage(start, end)


def parse_verse(text: str) -> VerseRef:
    """Parse a reference that must name exactly one verse (optionally with a part)."""
    p = parse_passage(text)
    if not p.is_single_verse:
        raise ValueError(f"Expected a single verse, got {text!r}")
    return p.start
