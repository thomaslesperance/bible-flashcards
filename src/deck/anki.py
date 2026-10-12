"""
Write a planned deck as an Anki package (.apkg) with genanki.

One note type with pre-rendered Front/Back HTML: each card is its own note, so
there are no siblings to bury. A note's `due` is its planned position, so Anki
introduces new cards in deck order. GUIDs derive from card keys, so a rebuilt
deck re-imports as updates instead of duplicates.
"""

import hashlib
from pathlib import Path

import genanki

from .order import Placed

ASSETS = Path(__file__).parent / "assets"
MODEL_ID = 1_607_202_610  # fixed: re-imports update the same note type


def stable_id(name: str) -> int:
    """A deck id that stays the same across builds of the same deck."""
    return 1_500_000_000 + int(hashlib.sha1(name.encode()).hexdigest(), 16) % 100_000_000


def note_model() -> genanki.Model:
    css = (ASSETS / "card.css").read_text(encoding="utf-8")
    js = (ASSETS / "card.js").read_text(encoding="utf-8")
    return genanki.Model(
        MODEL_ID, "Bible flashcards v2",
        fields=[{"name": "Key"}, {"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card", "qfmt": "{{Front}}\n<script>\n" + js + "</script>",
                    "afmt": "{{Back}}"}],
        css=css)


def write_package(placed: list[Placed], deck_name: str, description: str, path: Path) -> None:
    deck_id = stable_id(deck_name)
    deck = genanki.Deck(deck_id, deck_name, description)
    model = note_model()
    for p in placed:
        c = p.card
        deck.add_note(genanki.Note(
            model, [c.key, c.front, c.back], tags=c.tags + [f"day::{p.day:02d}"],
            guid=genanki.guid_for(deck_id, c.key), due=p.pos))
    genanki.Package(deck).write_to_file(str(path))
