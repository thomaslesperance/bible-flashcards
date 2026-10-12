"""
Canonical book table (Protestant 66-book canon).

Each book is identified by its OSIS ID (e.g. "Matt", "1Cor"), a widely used
standard that most public-domain Bible sources (USFM/OSIS exports, eBible.org,
etc.) can be mapped to. Testament is derived from the book, so it never needs
to be stored alongside verse text.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    osis: str
    usfm: str  # 3-character USFM code used by bible.eng.db / the Free Use Bible API, e.g. "MAT"
    name: str
    testament: str  # "old" | "new"
    index: int  # canonical order, 0-based
    aliases: tuple[str, ...]


_RAW = [
    # (osis, name, extra aliases)
    ("Gen", "Genesis", ("gn", "ge")),
    ("Exod", "Exodus", ("ex", "exo")),
    ("Lev", "Leviticus", ("lv",)),
    ("Num", "Numbers", ("nm", "nu")),
    ("Deut", "Deuteronomy", ("dt", "deu")),
    ("Josh", "Joshua", ("jos",)),
    ("Judg", "Judges", ("jdg", "jg")),
    ("Ruth", "Ruth", ("ru",)),
    ("1Sam", "1 Samuel", ("1sa",)),
    ("2Sam", "2 Samuel", ("2sa",)),
    ("1Kgs", "1 Kings", ("1ki", "1kg")),
    ("2Kgs", "2 Kings", ("2ki", "2kg")),
    ("1Chr", "1 Chronicles", ("1ch",)),
    ("2Chr", "2 Chronicles", ("2ch",)),
    ("Ezra", "Ezra", ("ezr",)),
    ("Neh", "Nehemiah", ("ne",)),
    ("Esth", "Esther", ("est",)),
    ("Job", "Job", ("jb",)),
    ("Ps", "Psalms", ("psalm", "psa", "pss")),
    ("Prov", "Proverbs", ("pr", "prv", "pro")),
    ("Eccl", "Ecclesiastes", ("ecc", "qoh")),
    ("Song", "Song of Solomon", ("songofsongs", "sos", "canticles")),
    ("Isa", "Isaiah", ("is",)),
    ("Jer", "Jeremiah", ("je",)),
    ("Lam", "Lamentations", ("la",)),
    ("Ezek", "Ezekiel", ("eze", "ezk")),
    ("Dan", "Daniel", ("dn", "da")),
    ("Hos", "Hosea", ("ho",)),
    ("Joel", "Joel", ("jl",)),
    ("Amos", "Amos", ("am",)),
    ("Obad", "Obadiah", ("ob",)),
    ("Jonah", "Jonah", ("jon", "jnh")),
    ("Mic", "Micah", ("mi",)),
    ("Nah", "Nahum", ("na",)),
    ("Hab", "Habakkuk", ("hb",)),
    ("Zeph", "Zephaniah", ("zep",)),
    ("Hag", "Haggai", ("hg",)),
    ("Zech", "Zechariah", ("zec",)),
    ("Mal", "Malachi", ("ml",)),
    ("Matt", "Matthew", ("mt", "mat")),
    ("Mark", "Mark", ("mk", "mrk")),
    ("Luke", "Luke", ("lk", "luk")),
    ("John", "John", ("jn", "jhn")),
    ("Acts", "Acts", ("ac",)),
    ("Rom", "Romans", ("rm", "ro")),
    ("1Cor", "1 Corinthians", ("1co",)),
    ("2Cor", "2 Corinthians", ("2co",)),
    ("Gal", "Galatians", ("ga",)),
    ("Eph", "Ephesians", ("ep",)),
    ("Phil", "Philippians", ("php", "pp")),
    ("Col", "Colossians", ("co",)),
    ("1Thess", "1 Thessalonians", ("1th",)),
    ("2Thess", "2 Thessalonians", ("2th",)),
    ("1Tim", "1 Timothy", ("1ti",)),
    ("2Tim", "2 Timothy", ("2ti",)),
    ("Titus", "Titus", ("tit",)),
    ("Phlm", "Philemon", ("phm", "philem")),
    ("Heb", "Hebrews", ()),
    ("Jas", "James", ("jm",)),
    ("1Pet", "1 Peter", ("1pe", "1pt")),
    ("2Pet", "2 Peter", ("2pe", "2pt")),
    ("1John", "1 John", ("1jn", "1jo")),
    ("2John", "2 John", ("2jn", "2jo")),
    ("3John", "3 John", ("3jn", "3jo")),
    ("Jude", "Jude", ("jud",)),
    ("Rev", "Revelation", ("rv", "re", "apocalypse")),
]

# Books with one chapter, where "Jude 3" means verse 3 rather than chapter 3.
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude"}

# USFM codes in the same canonical order as _RAW.
_USFM = (
    "GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO "
    "ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL "
    "MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB "
    "JAS 1PE 2PE 1JN 2JN 3JN JUD REV"
).split()
assert len(_USFM) == len(_RAW)

BOOKS: list[Book] = [
    Book(osis, usfm, name, "old" if i < 39 else "new", i, aliases)
    for i, ((osis, name, aliases), usfm) in enumerate(zip(_RAW, _USFM))
]
BY_OSIS: dict[str, Book] = {b.osis: b for b in BOOKS}
BY_USFM: dict[str, Book] = {b.usfm: b for b in BOOKS}


def _norm(s: str) -> str:
    """Lowercase and drop spaces/periods so '1 Cor.' and '1cor' compare equal."""
    return s.lower().replace(" ", "").replace(".", "")


_ALIASES: dict[str, Book] = {}
for _b in BOOKS:
    for _a in (_b.osis, _b.name, *_b.aliases):
        _ALIASES[_norm(_a)] = _b


def lookup_book(name: str) -> Book:
    """
    Resolve a book name/abbreviation to a Book.

    Tries exact aliases first, then falls back to a unique prefix of a full
    name or OSIS ID (e.g. "Matth" -> Matthew). Ambiguous prefixes such as
    "Ph" (Philippians/Philemon) raise rather than guess.
    """
    key = _norm(name)
    if key in _ALIASES:
        return _ALIASES[key]
    matches = {
        b.osis: b
        for b in BOOKS
        if len(key) >= 2 and (_norm(b.name).startswith(key) or _norm(b.osis).startswith(key))
    }
    if len(matches) == 1:
        return next(iter(matches.values()))
    if matches:
        raise ValueError(f"Ambiguous book name {name!r}: could be {', '.join(matches)}")
    raise ValueError(f"Unknown book name {name!r}")
