"""
Deck order: when each card is introduced (docs/method/sequence-v2.md §4 "Timing"
and the Appendix).

Anki introduces exactly N new cards a day in deck order, so "a day later" is
encoded as "at least N cards later". Each step places one group of cards:
1. a released group whose wait is over (oldest first);
2. else the next Phase 1 family;
3. else the next unit's wave 1, if fewer than MAX_ACTIVE units are in waves 1-2;
4. else the waiting group that's due soonest, pulled forward.

Phase 2 may start once every Phase 1 group has been *released*. The draft says
"once introduced"; waiting for that would pull the last List the parts / Whole
outline cards forward and lose their day of spacing, so text fills those gaps.
"""

import heapq
from dataclasses import dataclass, field
from itertools import count
from typing import Callable

from .cards import CONTEXT_CAP_WORDS, RECITE_CAP_WORDS, Card, CardBuilder
from .tree import Node, Unit

MAX_ACTIVE = 2


@dataclass(order=True)
class _Pending:
    ready_at: int
    seq: int
    name: str = field(compare=False)
    cards: list[Card] = field(compare=False)
    on_place: Callable[[], None] | None = field(compare=False, default=None)


@dataclass
class Placed:
    pos: int     # 0-based deck position
    day: int     # 1-based day it's introduced on
    group: str
    card: Card


class Planner:
    def __init__(self, root: Node, builder: CardBuilder, per_day: int = 12):
        self.root, self.b, self.n = root, builder, per_day
        self.placed: list[Placed] = []
        self.pending: list[_Pending] = []
        self.seq = count()
        self.active: set[str] = set()       # unit keys in waves 1-2
        self.units_done: set[str] = set()
        self.closed: set[str] = set()       # section keys whose closing group is placed
        self.listed: set[str] = set()       # family keys whose List the parts is placed
        self.wholes_released: set[str] = set()
        self.closing_released: set[str] = set()

    # ----------------------------------------------------------------- basics

    @property
    def pos(self) -> int:
        return len(self.placed)

    def _release(self, name, cards, delay_days: int, on_place=None):
        ready = self.pos + delay_days * self.n
        heapq.heappush(self.pending, _Pending(ready, next(self.seq), name, cards, on_place))

    def _place(self, name, cards, on_place=None):
        for c in cards:
            self.placed.append(Placed(self.pos, self.pos // self.n + 1, name, c))
        if on_place:
            on_place()

    # ----------------------------------------------------------------- Phase 1

    def _phase1_groups(self):
        """Breadth-first: Read-through (top level), Preview, and Outline clozes."""
        level = [self.root]
        while level:
            for node in level:
                cards = [self.b.read_through(node)] if node.depth == 1 else []
                if node.children:
                    cards += [self.b.preview(node)] + [self.b.outline_cloze(c) for c in node.children]
                if cards:
                    yield node, cards
            level = [c for n in level for c in n.children]

    def _after_intro(self, node: Node):
        if node.children:
            self._release(f"list the parts · {node.title}", [self.b.list_parts(node)], 1,
                          lambda: self._after_list(node))

    def _after_list(self, node: Node):
        self.listed.add(node.key)
        for s in node.path:
            families = [n for n in s.walk() if n.children]
            has_subsections = any(c.children for c in s.children)
            if (has_subsections and s.key not in self.wholes_released
                    and all(f.key in self.listed for f in families)):
                self.wholes_released.add(s.key)
                self._release(f"whole outline · {s.title}", [self.b.whole_outline(s)], 1)

    # ----------------------------------------------------------------- Phase 2

    def _wave1(self, unit: Unit):
        cards = [self.b.text_to_header(unit), self.b.missing_words(unit), self.b.first_letters(unit)]
        self.active.add(unit.key)
        self._place(f"wave 1 · {unit.key}", cards, lambda: self._after_wave1(unit))

    def _after_wave1(self, unit: Unit):
        if len(unit.verses) < 2:
            self.active.discard(unit.key)
            self._release_wave3(unit)
            return
        wave2 = [self.b.scaffolded_cloze(unit, v) for v in unit.verses]
        if len(unit.verses) >= 4:
            wave2.append(self.b.anchor_cloze(unit))
        self._release(f"wave 2 · {unit.key}", wave2, 1, lambda: self._after_wave2(unit))

    def _after_wave2(self, unit: Unit):
        self.active.discard(unit.key)
        self._release_wave3(unit)

    def _release_wave3(self, unit: Unit):
        self._release(f"wave 3 · {unit.key}", [self.b.header_to_text(unit)], 1,
                      lambda: self._after_wave3(unit))

    def _after_wave3(self, unit: Unit):
        self.units_done.add(unit.key)
        self._try_close(unit.node)

    def _try_close(self, node: Node | None):
        """Close `node` and then its ancestors, as soon as everything under each is done."""
        while node is not None:
            if node.is_section and node.key not in self.closing_released:
                units_done = all(u.key in self.units_done for n in node.walk() for u in n.units)
                kids_closed = all(c.key in self.closed for c in node.children if c.is_section)
                if not (units_done and kids_closed):
                    return
                self.closing_released.add(node.key)
                cards = [self.b.missing_section(node, i) for i, p in enumerate(node.parts)
                         if p.words <= RECITE_CAP_WORDS]
                if node.words > RECITE_CAP_WORDS:
                    cards.append(self.b.first_lines(node))
                self._release(f"closing · {node.title}", cards, 0,
                              lambda node=node: self._after_closing(node))
                return  # the parent is tried again once this closing group is placed
            node = node.parent

    def _after_closing(self, node: Node):
        self.closed.add(node.key)
        if node.words <= CONTEXT_CAP_WORDS:
            self._release(f"recite · {node.title}", [self.b.section_header_to_text(node)], 1)
        self._try_close(node.parent)

    # ----------------------------------------------------------------- driver

    def plan(self) -> list[Placed]:
        phase1 = self._phase1_groups()
        units = [u for n in self.root.walk() for u in n.units]
        next_phase1 = next(phase1, None)
        next_unit = 0
        while True:
            if self.pending and self.pending[0].ready_at <= self.pos:
                g = heapq.heappop(self.pending)
                self._place(g.name, g.cards, g.on_place)
            elif next_phase1 is not None:
                node, cards = next_phase1
                self._place(f"intro · {node.title}", cards, lambda node=node: self._after_intro(node))
                next_phase1 = next(phase1, None)
            elif next_unit < len(units) and len(self.active) < MAX_ACTIVE:
                self._wave1(units[next_unit])
                next_unit += 1
            elif self.pending:
                g = heapq.heappop(self.pending)  # nothing else to do: pull it forward
                self._place(g.name, g.cards, g.on_place)
            else:
                break
        missing = [u.key for u in units if u.key not in self.units_done]
        if missing:
            raise RuntimeError(f"Units never finished: {missing}")
        return self.placed
