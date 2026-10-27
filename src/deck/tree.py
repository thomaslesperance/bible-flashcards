"""
The outline as a tree, and its leaves split into units (docs/method/sequence-v2.md §4).

Terms:
- leaf: a header with no sub-headers; it holds verses directly.
- unit: the chunk of text learned as one piece -- a leaf, or one part of a long leaf.
- section: a header with sub-headers, or a leaf split into 2+ units. Its sub-headers
  (or units) are its parts.
"""

from dataclasses import dataclass, field
from itertools import count

import yaml

from ..books import lookup_book
from ..chapter import Heading, ParagraphBreak, Subtitle, Verse, load_chapter
from ..refs import VerseRef

UNIT_TARGET_WORDS = 80
UNIT_MAX_WORDS = 130
MID_STANZA_PENALTY = 400  # cost of cutting inside a paragraph, in squared words (~20 words off target)


def words(verses: list[Verse]) -> int:
    return sum(v.word_count for v in verses)


def vref(v: Verse) -> str:
    return f"{v.ref.chapter}:{v.ref.verse}"


def fmt_range(verses: list[Verse]) -> str:
    a, b = verses[0].ref, verses[-1].ref
    if a == b:
        return f"{a.chapter}:{a.verse}"
    if a.chapter == b.chapter:
        return f"{a.chapter}:{a.verse}–{b.verse}"
    return f"{a.chapter}:{a.verse}–{b.chapter}:{b.verse}"


def _label(depth: int, i: int) -> str:
    roman = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]
    if depth == 1:
        return str(i + 1)
    if depth == 2:
        return "abcdefghijklmnopqrstuvwxyz"[i]
    if depth == 3:
        return roman[i]
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]


@dataclass
class Text:
    """A passage's verses in reading order, and the verses that start a paragraph."""
    translation: str
    verses: list[Verse]
    breaks: set[VerseRef]  # after a ParagraphBreak or Heading block, or first in its chapter


def load_text(translation: str, book: str, chapters: range) -> Text:
    """`book` is an OSIS ID ("Isa")."""
    verses, breaks = [], set()
    for ch in chapters:
        pending = True
        for block in load_chapter(translation, book, ch).blocks:
            if isinstance(block, (Heading, ParagraphBreak, Subtitle)):
                pending = True
            elif isinstance(block, Verse):
                if pending:
                    breaks.add(block.ref)
                pending = False
                verses.append(block)
    return Text(translation, verses, breaks)


@dataclass(eq=False)
class Unit:
    key: str  # "u01", ...
    node: "Node"  # the leaf it belongs to
    index: int  # 0-based position within the leaf
    verses: list[Verse]

    @property
    def count(self) -> int:
        return len(self.node.units)

    @property
    def title(self) -> str:
        if self.count == 1:
            return self.node.title
        return f"{self.node.title} · part {self.index + 1} of {self.count}"

    @property
    def ref(self) -> str:
        return fmt_range(self.verses)

    @property
    def words(self) -> int:
        return words(self.verses)


@dataclass(eq=False)
class Node:
    key: str  # "n01", ...
    title: str
    verses: list[Verse]
    parent: "Node | None" = None
    depth: int = 0
    label: str = ""
    bsb_heading: str | None = None
    children: list["Node"] = field(default_factory=list)
    units: list[Unit] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return not self.children

    @property
    def parts(self) -> list:
        """Sub-headers, or the units of a split leaf; empty for a one-unit leaf."""
        if self.children:
            return self.children
        return self.units if len(self.units) > 1 else []

    @property
    def is_section(self) -> bool:
        return bool(self.parts)

    @property
    def ref(self) -> str:
        return fmt_range(self.verses)

    @property
    def words(self) -> int:
        return words(self.verses)

    @property
    def path(self) -> list["Node"]:
        """Root ... self."""
        node, out = self, []
        while node:
            out.append(node)
            node = node.parent
        return out[::-1]

    def walk(self):
        """Pre-order: self, then each child's subtree."""
        yield self
        for c in self.children:
            yield from c.walk()

    def header_count(self) -> int:
        return sum(1 for _ in self.walk())


def _parse_point(text: str) -> tuple[int, int]:
    ch, v = str(text).split(":")
    return int(ch), int(v)


def load_tree(outline_path, translation: str = "BSB") -> tuple[Node, Text]:
    """
    Build the tree from an outline YAML (same shape as outlines.yml) and load its
    text. If the book holds exactly one top section, that section is the root.
    """
    with open(outline_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    (book_name, body), = spec.items()
    first, last = (_parse_point(p) for p in body["ref"].split("-"))
    text = load_text(translation, lookup_book(book_name).osis, range(first[0], last[0] + 1))
    by_point = {(v.ref.chapter, v.ref.verse): v for v in text.verses}

    def verses_of(ref: str) -> list[Verse]:
        a, b = (_parse_point(p) for p in ref.split("-"))
        out = [v for k, v in by_point.items() if a <= k <= b]
        if not out or (out[0].ref.chapter, out[0].ref.verse) != a or (out[-1].ref.chapter, out[-1].ref.verse) != b:
            raise ValueError(f"{ref} isn't fully covered by the loaded text")
        return out

    if len(body.get("sections") or {}) == 1:
        (title, body), = body["sections"].items()
    else:
        title = book_name
    ids = count(1)

    def build(title, spec, parent, depth, index):
        node = Node(f"n{next(ids):02d}", title, verses_of(spec["ref"]), parent, depth,
                    _label(depth, index) if depth else "", spec.get("bsb_heading"))
        for i, (t, s) in enumerate((spec.get("sections") or {}).items()):
            node.children.append(build(t, s, node, depth + 1, i))
        if node.children and [v for c in node.children for v in c.verses] != node.verses:
            raise ValueError(f"The parts of {title!r} don't exactly cover {spec['ref']}")
        return node

    root = build(title, body, None, 0, 0)
    unit_ids = count(1)
    for node in root.walk():
        if node.is_leaf:
            for i, chunk in enumerate(split_leaf(node.verses, text.breaks)):
                node.units.append(Unit(f"u{next(unit_ids):02d}", node, i, chunk))
    return root, text


def split_leaf(verses: list[Verse], breaks: set[VerseRef], target: int = UNIT_TARGET_WORDS,
               max_words: int = UNIT_MAX_WORDS) -> list[list[Verse]]:
    """
    Split a leaf into units near `target` words, none over `max_words` (unless a
    single verse is). Cuts fall between paragraphs where possible: a paragraph over
    `max_words` is broken into verses, and each cut inside a paragraph costs
    MID_STANZA_PENALTY. The split with the lowest total cost wins.
    """
    if words(verses) <= max_words:
        return [verses]
    paragraphs: list[list[Verse]] = []
    for v in verses:
        if v.ref in breaks or not paragraphs:
            paragraphs.append([v])
        else:
            paragraphs[-1].append(v)
    pieces: list[list[Verse]] = []
    for p in paragraphs:
        pieces.extend([[v] for v in p] if words(p) > max_words else [p])

    n = len(pieces)
    best = [0.0] + [float("inf")] * n  # best[j]: cost of splitting pieces[:j]
    cut = [0] * (n + 1)
    for j in range(1, n + 1):
        w = 0
        for i in range(j - 1, -1, -1):
            w += words(pieces[i])
            if w > max_words and i < j - 1:
                break
            cost = best[i] + (w - target) ** 2
            if i > 0 and pieces[i][0].ref not in breaks:
                cost += MID_STANZA_PENALTY
            if cost < best[j]:
                best[j], cut[j] = cost, i
    bounds, j = [], n
    while j > 0:
        bounds.append((cut[j], j))
        j = cut[j]
    return [[v for p in pieces[i:j] for v in p] for i, j in reversed(bounds)]
