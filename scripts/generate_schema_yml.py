#!/usr/bin/env python3
"""
Generates data/bible.eng.yml by querying data/bible.eng.db using functions from src.db.
"""

import os
import sys
import yaml
from pathlib import Path

# Ensure workspace root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src import db

# Ensure db module points to bible.eng.db
DB_FILE = BASE_DIR / "data" / "bible.eng.db"
OUTPUT_FILE = BASE_DIR / "data" / "bible.eng.yml"

if hasattr(db, 'set_db_path'):
    db.set_db_path(str(DB_FILE))
else:
    db.DB_PATH = str(DB_FILE)


TABLE_DESCRIPTIONS = {
    "Book": (
        "Books of the Bible associated with specific translations. Contains canonical order, "
        "book identifiers (e.g., 'GEN', 'MAT'), titles, chapter counts, apocrypha flags, "
        "and denormalized translation metadata."
    ),
    "Chapter": (
        "Chapter-level scripture containers for each book and translation. Stores complete "
        "chapter contents in structured JSON format (headings, verses, paragraph breaks), "
        "along with translation metadata."
    ),
    "ChapterAudioTiming": (
        "Verse- and phrase-level timestamp markers for spoken Bible narration per chapter, "
        "book, reader, and translation. Facilitates synchronized audio playback and read-along highlighting."
    ),
    "ChapterAudioUrl": (
        "Streaming and download audio URLs for Bible chapters, partitioned by reader/narrator "
        "(e.g., 'david'), translation, book, and chapter number. URLs link to audio files hosted on helloao.org."
    ),
    "ChapterFootnote": (
        "Footnotes, textual variants (e.g., LXX differences), translation notes, and cross-reference "
        "annotations associated with specific chapters and verses across translations."
    ),
    "ChapterVerse": (
        "Granular verse-level scripture records. Stores plain text verses, structured JSON payloads "
        "('contentJson') with formatting/markup, and denormalized translation details."
    ),
    "ChapterWords": (
        "Tokenized word mappings and character-range alignments per chapter ('wordsJson') linking "
        "words to start/end character offsets and verse locations for concordances and word tracking."
    ),
    "Commentary": (
        "Catalog of Bible commentary works available in the database (e.g., Matthew Henry, Adam Clarke, "
        "John Calvin, Keil & Delitzsch, Jamieson-Fausset-Brown, John Gill, and Tyndale Open Study Notes). "
        "Stores author/work titles, language, website URLs, and licensing terms."
    ),
    "CommentaryBook": (
        "Book-level introductions, historical prefaces, outlines, and chapter coverage for each commentary work."
    ),
    "CommentaryChapter": (
        "Chapter-level commentary overviews, section outlines, and structured chapter commentary in JSON format."
    ),
    "CommentaryChapterVerse": (
        "Verse-by-verse expository commentary text and structured JSON paragraphs explaining individual verses."
    ),
    "Dataset": (
        "Registry of external auxiliary Bible study datasets, such as the OpenBible.info cross-reference "
        "dataset ('open-cross-ref'). Stores source URLs, language, and attribution licenses."
    ),
    "DatasetBook": (
        "Book-level partitioning and coverage statistics for auxiliary study datasets, including canonical order "
        "and chapter counts."
    ),
    "DatasetChapter": (
        "Chapter-level data payloads and structured JSON cross-reference collections for auxiliary study datasets."
    ),
    "DatasetChapterVerse": (
        "Verse-level data payloads and structured JSON cross-references for individual verses in auxiliary study datasets."
    ),
    "DatasetReference": (
        "Granular scripture cross-reference mappings connecting source verses to referenced verses. "
        "Includes source verse coordinates, target reference coordinates (with optional end-verse ranges), "
        "and relevance/confidence vote scores."
    ),
    "Translation": (
        "Registry of the 51 English Bible translations present in the database (e.g., Berean Standard Bible 'BSB', "
        "World English Bible 'ENGWEBP', King James Version, American Standard Version). Stores translation identifiers, "
        "short names, language codes, text direction, websites, and license notices."
    ),
    "_prisma_migrations": (
        "Internal Prisma ORM schema migration ledger tracking database schema migration history, checksums, "
        "execution timestamps, logs, and applied steps."
    ),
}

COLUMN_DESCRIPTIONS = {
    # Common / Shared
    "id": "Primary identifier or slug.",
    "translationId": "Foreign identifier matching Translation.id (e.g., 'BSB', 'ENGWEBP').",
    "bookId": "Standard book code (e.g., 'GEN', '1CH', 'MAT', 'REV').",
    "commentaryId": "Foreign identifier matching Commentary.id (e.g., 'adam-clarke', 'matthew-henry').",
    "datasetId": "Foreign identifier matching Dataset.id (e.g., 'open-cross-ref').",
    "name": "Standard name or title.",
    "commonName": "Common English name.",
    "title": "Title heading.",
    "order": "Canonical integer order index (1-based).",
    "numberOfChapters": "Total number of chapters in this book.",
    "isApocryphal": "Numeric boolean flag (1 if apocryphal / deuterocanonical, 0 otherwise).",
    "number": "Chapter or verse sequence number.",
    "chapterNumber": "Chapter sequence number within the book.",
    "verseNumber": "Verse sequence number within the chapter.",
    "text": "Plain text content.",
    "json": "Serialized JSON containing structured content and formatting.",
    "contentJson": "Serialized JSON array or object containing rich text blocks.",
    "wordsJson": "Serialized JSON mapping word tokens and character offsets to verses.",
    "timingsJson": "Serialized JSON array of audio timing markers and verse offsets.",
    "reader": "Narrator or voice identifier for the audio recording.",
    "url": "HTTP URL pointing to the resource (e.g., audio file).",
    "website": "Source or publisher website URL.",
    "licenseUrl": "URL containing full license and usage terms.",
    "licenseNotes": "Additional notes regarding licensing or modifications made.",
    "licenseNotice": "Legal copyright notice and required attribution statement.",
    "shortName": "Abbreviated name or translation acronym.",
    "englishName": "Full name in English.",
    "language": "ISO language code (e.g., 'eng').",
    "textDirection": "Text reading direction ('ltr' for left-to-right, 'rtl' for right-to-left).",
    "sha256": "SHA-256 cryptographic checksum of data payload.",
    "introduction": "Introductory or preface text.",
    "introductionSummary": "Short summary of the introductory text.",
    "referenceBookId": "Target cross-reference book code.",
    "referenceChapter": "Target cross-reference chapter number.",
    "referenceVerse": "Target cross-reference starting verse number.",
    "endVerseNumber": "Target cross-reference ending verse number (null if single verse).",
    "score": "Relevance or confidence vote score for the cross-reference.",
    
    # Denormalized export columns (aliased by importer)
    "id:1": "Denormalized parent entity ID (e.g., joined Translation.id, Commentary.id, or Dataset.id).",
    "name:1": "Denormalized parent entity name.",
    "sha256:1": "Denormalized parent entity SHA-256 checksum.",
    
    # _prisma_migrations
    "checksum": "Prisma migration file checksum.",
    "finished_at": "Timestamp when migration completed execution.",
    "migration_name": "Unique migration directory/script name.",
    "logs": "Execution logs or error messages during migration.",
    "rolled_back_at": "Timestamp when migration was rolled back (null if active).",
    "started_at": "Timestamp when migration execution commenced.",
    "applied_steps_count": "Number of migration operations applied in this migration step.",
}


def main():
    print(f"Connecting to {DB_FILE} using src.db...")
    
    # Fetch all user tables
    table_rows = db.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name;"
    )
    
    tables_yaml_data = {}
    
    for row in table_rows:
        table_name = row["name"]
        
        # Row count
        cnt_row = db.fetch_one(f"SELECT COUNT(*) AS cnt FROM '{table_name}';")
        row_count = cnt_row["cnt"] if cnt_row else 0
        
        # Columns via PRAGMA
        cols_rows = db.fetch_all(f"PRAGMA table_info('{table_name}');")
        
        columns_list = []
        for col in cols_rows:
            col_name = col["name"]
            col_type = col["type"] or "TEXT"
            col_info = {
                "name": col_name,
                "type": col_type,
            }
            if col["pk"]:
                col_info["primary_key"] = True
            if col["notnull"]:
                col_info["nullable"] = False
                
            if col_name in COLUMN_DESCRIPTIONS:
                col_info["description"] = COLUMN_DESCRIPTIONS[col_name]
                
            columns_list.append(col_info)
            
        table_entry = {
            "description": TABLE_DESCRIPTIONS.get(table_name, f"Table storing {table_name} data."),
            "row_count": row_count,
            "columns": columns_list,
        }
        tables_yaml_data[table_name] = table_entry
        
    db_schema = {
        "database": "data/bible.eng.db",
        "format": "SQLite 3",
        "description": (
            "Comprehensive English Bible database containing 51 English translations, "
            "7 commentaries, cross-reference datasets, verse-level text, audio links, and concordances."
        ),
        "total_tables": len(tables_yaml_data),
        "tables": tables_yaml_data,
    }
    
    # Custom representer for neat multi-line string formatting
    class IndentedDumper(yaml.Dumper):
        def represent_scalar(self, tag, value, style=None):
            if "\n" in value:
                style = "|"
            return super().represent_scalar(tag, value, style)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(db_schema, f, Dumper=IndentedDumper, sort_keys=False, allow_unicode=True, indent=2)
        
    print(f"Successfully generated {OUTPUT_FILE} ({len(tables_yaml_data)} tables documented).")


if __name__ == "__main__":
    main()
