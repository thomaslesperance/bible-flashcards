"""
One builder per card type of the v2 sequence (docs/method/sequence-v2.md §2–4).
Each returns a Card with its front and back HTML; order.py decides when it's introduced.
"""

from dataclasses import dataclass, field
from html import escape

from ..chapter import Verse
from . import render as r
from .tree import Node, Text, Unit, fmt_range, vref

RECITE_CAP_WORDS = 280    # Missing section parts and the First lines threshold (~2 min aloud)
CONTEXT_CAP_WORDS = 450   # Missing section shows all sibling text; Section header -> text (~3 min)


@dataclass
class Card:
    key: str     # stable id; the note's GUID is derived from it
    kind: str    # card type slug, also a tag
    phase: int
    about: str   # one line for the CSVs
    front: str
    back: str
    tags: list[str] = field(default_factory=list)


def _tag(s: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in s.lower()).strip("-")


class CardBuilder:
    def __init__(self, root: Node, text: Text, credit: str = ""):
        self.root, self.text = root, text
        self._pos = {v.ref: i for i, v in enumerate(text.verses)}
        self.credit = f'<div class="credit">{escape(credit)}</div>' if credit else ""

    def _passage(self, verses: list[Verse], **kw) -> str:
        return r.passage(verses, self.text.breaks, **kw)

    def _card(self, kind, phase, key, about, front, back, item=None) -> Card:
        tags = [f"phase::{phase}", f"type::{kind}"]
        if isinstance(item, Unit):
            tags.append(f"unit::{item.key}")
        elif isinstance(item, Node):
            tags.append(f"section::{_tag(item.title)}")
        return Card(f"{kind}:{key}", kind, phase, about, front, back, tags)

    def _neighbours(self, verses: list[Verse]) -> tuple[Verse | None, Verse | None]:
        a, b = self._pos[verses[0].ref], self._pos[verses[-1].ref]
        all_verses = self.text.verses
        return (all_verses[a - 1] if a > 0 else None,
                all_verses[b + 1] if b + 1 < len(all_verses) else None)

    @staticmethod
    def _headings_under(node: Node) -> dict:
        """{first verse: title} for every header below `node` (shallowest wins)."""
        heads = {}
        for n in node.walk():
            if n is not node:
                heads.setdefault(n.verses[0].ref, n.title)
        return heads

    # ---------------------------------------------------------------- Phase 1

    def read_through(self, node: Node) -> Card:
        body = (r.outline_map(self.root, node, highlight=[node])
                + self._passage(node.verses, headings=self._headings_under(node)))
        front = r.frame("read", f"READ ALOUD · {escape(node.ref)}", body,
                        sub=f"<b>{escape(node.title)}</b> — read it through once, aloud, start to finish.")
        return self._card("read-through", 1, node.key, f"Read {node.title} ({node.ref})",
                          front, front + r.RUBRIC_READ + self.credit, node)

    def preview(self, node: Node) -> Card:
        front = r.frame("outline", f"PREVIEW · {escape(node.title)}",
                        r.outline_map(self.root, node, highlight=node.children),
                        sub=f"Its {len(node.children)} parts, in order. Read them through.")
        return self._card("preview", 1, node.key, f"Preview {node.title}", front,
                          front + r.RUBRIC_READ, node)

    def outline_cloze(self, node: Node) -> Card:
        # Focus on the parent so the blank's own sub-headers stay collapsed (they'd hint).
        def side(reveal):
            return r.frame("outline", "OUTLINE · what goes in the blank?",
                           r.outline_map(self.root, node.parent, blank=node, reveal=reveal))
        return self._card("outline-cloze", 1, node.key, f"Cloze: {node.title}",
                          side(False), side(True) + r.RUBRIC, node)

    def list_parts(self, node: Node) -> Card:
        sub = f"List the {len(node.children)} parts of <b>{escape(node.title)}</b>, in order."
        def side(reveal):
            return r.frame("outline", "OUTLINE · list the parts",
                           r.outline_map(self.root, node, hide_parts=node, reveal=reveal,
                                         highlight=node.children if reveal else ()), sub=sub)
        return self._card("list-parts", 1, node.key, f"List the parts of {node.title}",
                          side(False), side(True) + r.RUBRIC, node)

    def whole_outline(self, node: Node) -> Card:
        n = node.header_count() - 1
        sub = f"Recite the whole outline of <b>{escape(node.title)}</b> — {n} headers, in order."
        front = r.frame("outline", "OUTLINE · the whole outline",
                        r.outline_map(self.root, node, hide_parts=node,
                                      hidden_label=f"{n} headers at every level"), sub=sub)
        below = [x for x in node.walk() if x is not node]
        back = r.frame("outline", "OUTLINE · the whole outline",
                       r.outline_map(self.root, node, expand_under=node, highlight=below), sub=sub)
        return self._card("whole-outline", 1, node.key, f"Whole outline of {node.title}",
                          front, back + r.RUBRIC, node)

    # ---------------------------------------------------------------- Phase 2: unit ladder

    def text_to_header(self, unit: Unit) -> Card:
        front = r.frame("ladder", "WHERE DOES THIS BELONG?", self._passage(unit.verses))
        node = unit.node
        crumbs = " › ".join(escape(n.title) for n in node.path[:-1])
        part = f" · part {unit.index + 1} of {unit.count}" if unit.count > 1 else ""
        answer = (f'<div class="answer"><div class="crumbs">{crumbs}</div>'
                  f'<div class="big">{escape(node.title)}</div>'
                  f'<div class="ref">{escape(unit.ref)}{part}</div></div>')
        back = r.frame("ladder", "WHERE DOES THIS BELONG?",
                       answer + r.outline_map(self.root, node, highlight=[node], unit=unit)
                       + self._passage(unit.verses))
        return self._card("text-to-header", 2, unit.key, f"Where does {unit.ref} belong?",
                          front, back + r.RUBRIC, unit)

    def missing_words(self, unit: Unit) -> Card:
        hide = lambda i: "blank" if i % 3 else "show"  # every 2nd and 3rd word
        def side(reveal):
            return r.frame("ladder", f"MISSING WORDS · {escape(unit.ref)}",
                           r.map_strip(self.root, unit)
                           + self._passage(unit.verses, word_mode=hide, reveal=reveal))
        return self._card("missing-words", 2, unit.key, f"Missing words {unit.ref}",
                          side(False), side(True) + r.RUBRIC_SCAFFOLD, unit)

    def first_letters(self, unit: Unit) -> Card:
        def side(reveal):
            return r.frame("ladder", f"FIRST LETTERS · {escape(unit.ref)}",
                           r.map_strip(self.root, unit)
                           + self._passage(unit.verses, word_mode=lambda i: "first", reveal=reveal))
        return self._card("first-letters", 2, unit.key, f"First letters {unit.ref}",
                          side(False), side(True) + r.RUBRIC_SCAFFOLD, unit)

    def _in_context(self, unit: Unit, verse_mode, reveal: bool) -> str:
        """The unit with the verse before and after it, dimmed."""
        before, after = self._neighbours(unit.verses)
        shown = ([before] if before else []) + unit.verses + ([after] if after else [])
        inside = {v.ref for v in unit.verses}
        return self._passage(shown, reveal=reveal,
                             verse_mode=lambda v: verse_mode(v) if v.ref in inside else "dim")

    def scaffolded_cloze(self, unit: Unit, verse: Verse) -> Card:
        def side(reveal):
            body = self._in_context(unit, lambda v: "block" if v is verse else "show", reveal)
            return r.frame("ladder", f"FILL THE GAP · recite {vref(verse)}",
                           r.map_strip(self.root, unit) + body)
        return self._card("scaffolded-cloze", 2, f"{unit.key}:{vref(verse)}",
                          f"Recite {vref(verse)} in {unit.ref}", side(False), side(True) + r.RUBRIC, unit)

    def anchor_cloze(self, unit: Unit) -> Card:
        middle = unit.verses[1:-1]
        ends = {unit.verses[0].ref, unit.verses[-1].ref}
        def side(reveal):
            body = self._in_context(unit, lambda v: "show" if v.ref in ends else "block", reveal)
            return r.frame("ladder", f"FILL THE MIDDLE · recite {escape(fmt_range(middle))}",
                           r.map_strip(self.root, unit) + body)
        return self._card("anchor-cloze", 2, unit.key, f"Recite the middle of {unit.ref}",
                          side(False), side(True) + r.RUBRIC, unit)

    def header_to_text(self, unit: Unit) -> Card:
        sub = (f"<b>{escape(unit.title)}</b> — {escape(r.verses_label(unit.verses))}. "
               f"Say it aloud, or type first letters.")
        typer = ('<div class="tm-box"><div class="tm-bar">'
                 '<button type="button" class="tm-go">Type first letters</button>'
                 '<button type="button" class="tm-hint">Hint</button></div>'
                 '<input class="tm-in" type="text" autocomplete="off" autocapitalize="off" '
                 'autocorrect="off" spellcheck="false" aria-label="Type the first letter of each word">'
                 f'<div class="tm-text">{self._passage(unit.verses, word_mode=lambda i: "type")}</div>'
                 '<div class="tm-score"></div></div>')
        def side(body):
            return r.frame("ladder", f"RECITE · {escape(unit.ref)}",
                           r.map_strip(self.root, unit) + body, sub=sub)
        return self._card("header-to-text", 2, unit.key, f"Recite {unit.title} ({unit.ref})",
                          side(typer), side(self._passage(unit.verses)) + r.RUBRIC, unit)

    # ---------------------------------------------------------------- Phase 2: section closing

    @staticmethod
    def _part_label(section: Node, i: int) -> str:
        p = section.parts[i]
        name = p.title if isinstance(p, Node) else f"Part {i + 1} of {len(section.parts)}"
        return f"{name} · {r.verses_label(p.verses)}"

    def missing_section(self, section: Node, i: int) -> Card:
        part = section.parts[i]
        label = self._part_label(section, i)
        first, last = self._pos[part.verses[0].ref], self._pos[part.verses[-1].ref]

        def side(reveal):
            if section.words <= CONTEXT_CAP_WORDS:  # the whole section around the gap
                before = [v for v in section.verses if self._pos[v.ref] < first]
                after = [v for v in section.verses if self._pos[v.ref] > last]
                dim = False
            else:  # too long to show: just the verse on each side
                b, a = self._neighbours(part.verses)
                before, after, dim = [b] if b else [], [a] if a else [], True
            mode = lambda v: "dim" if dim else "show"
            body = self._passage(before, verse_mode=mode) if before else ""
            body += r.gap_box(label, self._passage(part.verses, verse_mode=lambda v: "block",
                                                   reveal=reveal))
            body += self._passage(after, verse_mode=mode) if after else ""
            return r.frame("section", f"MISSING SECTION · {escape(section.title)}",
                           r.map_strip(self.root, section) + body)
        return self._card("missing-section", 2, f"{section.key}:{i + 1}",
                          f"Missing {label} in {section.title}", side(False), side(True) + r.RUBRIC,
                          section)

    def first_lines(self, section: Node) -> Card:
        def side(reveal):
            rows = []
            for i, p in enumerate(section.parts):
                line = (f'<span class="fl-a">{escape(r.first_line(p.verses))}</span>' if reveal
                        else '<span class="fl-q">…</span>')
                rows.append(f'<div class="fl-row"><div class="fl-h">'
                            f'{escape(self._part_label(section, i))}</div>{line}</div>')
            return r.frame("section", f"FIRST LINES · {escape(section.title)}",
                           r.map_strip(self.root, section) + f'<div class="fl-list">{"".join(rows)}</div>',
                           sub="How does each part begin?")
        return self._card("first-lines", 2, section.key, f"First lines of {section.title}",
                          side(False), side(True) + r.RUBRIC, section)

    def section_header_to_text(self, section: Node) -> Card:
        minutes = max(1, round(section.words / 150))  # ~150 words a minute aloud
        sub = (f"<b>{escape(section.title)}</b> — {escape(r.verses_label(section.verses))}, "
               f"about {minutes} min aloud.")
        if section.children:
            heads = self._headings_under(section)
        else:
            heads = {u.verses[0].ref: f"Part {i + 1}" for i, u in enumerate(section.units)}
        def side(body):
            return r.frame("section", f"RECITE THE SECTION · {escape(section.ref)}",
                           r.map_strip(self.root, section) + body, sub=sub)
        return self._card("section-header-to-text", 2, section.key, f"Recite {section.title}",
                          side(""), side(self._passage(section.verses, headings=heads)) + r.RUBRIC,
                          section)
