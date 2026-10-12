"""
Checks for the text parser and the v2 deck generator, on trial 2's outline.

    venv/bin/python -m unittest discover -s tests -t .

Reads data/bible.eng.db (read-only queries); writes nothing.
"""

import re
import unittest
from pathlib import Path

from src.chapter import load_chapter
from src.db import fetch_all
from src.deck.cards import CardBuilder
from src.deck.order import Planner
from src.deck.tree import UNIT_MAX_WORDS, load_tree

OUTLINE = Path(__file__).resolve().parent.parent / "data" / "outlines" / "isaiah_40_44.yml"


def squash(s: str) -> str:
    return " ".join(s.split())


class ChapterParserTest(unittest.TestCase):
    def test_text_matches_plain_verse_text(self):
        for ch in range(40, 45):
            chapter = load_chapter("BSB", "Isa", ch)
            rows = fetch_all("SELECT number, text FROM ChapterVerse WHERE translationId = 'BSB' "
                             "AND bookId = 'ISA' AND chapterNumber = ? ORDER BY number", (ch,))
            self.assertEqual([v.ref.verse for v in chapter.verses], [r["number"] for r in rows])
            for v, r in zip(chapter.verses, rows):
                self.assertEqual(squash(v.text), squash(r["text"]), f"Isa {ch}:{v.ref.verse}")


class DeckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root, cls.text = load_tree(OUTLINE)
        cls.placed = Planner(cls.root, CardBuilder(cls.root, cls.text), per_day=12).plan()
        cls.pos = {p.card.key: p.pos for p in cls.placed}

    def test_units_cover_each_leaf_in_order(self):
        for node in self.root.walk():
            if node.is_leaf:
                self.assertEqual([v for u in node.units for v in u.verses], node.verses)
                for u in node.units:
                    self.assertTrue(u.words <= UNIT_MAX_WORDS or len(u.verses) == 1, u.ref)

    def test_every_card_placed_once_with_n_per_day(self):
        keys = [p.card.key for p in self.placed]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual([p.pos for p in self.placed], list(range(len(self.placed))))
        self.assertTrue(all(p.day == p.pos // 12 + 1 for p in self.placed))

    def test_outline_is_introduced_before_any_text(self):
        first_text = min(p.pos for p in self.placed if p.card.phase == 2)
        intro = [p.pos for p in self.placed if p.group.startswith("intro · ")]
        self.assertLess(max(intro), first_text)

    def test_unit_ladder_order(self):
        for node in self.root.walk():
            for u in node.units:
                w1 = [self.pos[f"{k}:{u.key}"] for k in ("text-to-header", "missing-words", "first-letters")]
                self.assertEqual(w1, sorted(w1))
                w2 = [self.pos[f"scaffolded-cloze:{u.key}:{v.ref.chapter}:{v.ref.verse}"] for v in u.verses]
                w3 = self.pos[f"header-to-text:{u.key}"]
                self.assertLess(max(w1), min(w2))
                self.assertLess(max(w2), w3)

    def test_sections_close_after_their_text(self):
        for node in self.root.walk():
            if not node.is_section:
                continue
            closing = [p.pos for p in self.placed if p.group == f"closing · {node.title}"]
            self.assertTrue(closing, node.title)
            last_recite = max(self.pos[f"header-to-text:{u.key}"] for n in node.walk() for u in n.units)
            self.assertGreater(min(closing), last_recite)

    def test_missing_words_hides_every_2nd_and_3rd_word(self):
        unit = self.root.children[0].children[0].units[0]  # Isa 40:1–5
        card = next(p.card for p in self.placed if p.card.key == f"missing-words:{unit.key}")
        hidden = len(re.findall(r'class="mw"', card.front))
        self.assertEqual(hidden, unit.words - -(-unit.words // 3))  # words minus ceil(words / 3)
        self.assertEqual(len(re.findall(r'class="mw rv"', card.back)), hidden)


if __name__ == "__main__":
    unittest.main()
