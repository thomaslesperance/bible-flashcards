import yaml
import json
import csv
from pathlib import Path

# Paths relative to the script location
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "bible_sample.json"
OUTLINE_PATH = BASE_DIR / "data" / "outlines" / "sermon_on_the_mount.yml"
OUTPUT_DIR = BASE_DIR / "output"

def load_data():
    with open(RAW_DATA_PATH, 'r', encoding='utf-8') as f:
        bible = json.load(f)
    with open(OUTLINE_PATH, 'r', encoding='utf-8') as f:
        outline = yaml.safe_load(f)
    return bible, outline

def compile_anki_deck():
    print("Loading data...")
    bible, outline = load_data()
    print(f"Loaded {len(bible)} verses and the outline successfully.")
    
    print("\nStarting compilation pipeline...")
    # TODO: Implement tree traversal using functions from schemas.py
    
    print("\nCompilation finished. CSVs ready in the output directory.")

if __name__ == "__main__":
    compile_anki_deck()
