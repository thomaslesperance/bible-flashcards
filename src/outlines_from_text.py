"""Build data/outlines/outlines.yml from the hand-corrected outline text.

The text gives each book name flush left, then one entry per line indented two
spaces per level:

    Genesis
      1. God and the World  ( 1:1-10:32 )
        a. The Creation of the Heavens and the Earth  ( 1:1-2:3 )

Depth comes straight from the indentation, so unlike the PDF there is nothing
to infer. The numbering cycle and the verse ranges are still checked, and the
output has the same shape as bsb_book_outlines.yml.
"""
import re
import sys
from pathlib import Path

import yaml

from parse_book_outlines import (
    BOOKS, count, find_problems, numbering_kind, parse_range, read_marker,
    set_book_span, to_mapping, warnings,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_TEXT = BASE_DIR / "data" / "raw" / "bsb_book_outlines_corrected.txt"
OUTPUT_PATH = BASE_DIR / "data" / "outlines" / "outlines.yml"

INDENT = 2
# The closing parenthesis is optional: a few hand-edited lines drop it.
ENTRY = re.compile(r"^( *)([0-9]+|[a-z]+)\.\s+(.+?)\s+\(([^()]*)\)?\s*$")


def parse(path):
    text = path.read_text(encoding="utf-8")
    text = text.replace("⁠", "").replace(" ", " ")
    tree, stack, counters = {}, [], {}

    for lineno, line in enumerate(text.split("\n"), 1):
        if not line.strip():
            continue
        where = f"line {lineno}"
        if not line.startswith(" "):
            name = line.strip()
            if name not in BOOKS:
                warnings.append(f"{where}: {name!r} is not a book name")
            root = {"title": name, "marker": None, "ref": None, "span": None,
                    "children": [], "page": None}
            tree[name] = root
            stack = [root]
            continue
        if not stack:
            warnings.append(f"{where}: entry before any book name")
            continue

        m = ENTRY.match(line)
        if not m:
            warnings.append(f"{where}: unrecognised line {line.strip()!r}")
            continue
        indent, tok, title, rng = m.groups()
        if not line.rstrip().endswith(")"):
            warnings.append(f"{where}: missing closing ')' (read anyway)")
        if len(indent) % INDENT:
            warnings.append(f"{where}: indent of {len(indent)} is not a "
                            f"multiple of {INDENT}")
        depth = len(indent) // INDENT - 1
        if depth > len(stack) - 1:
            warnings.append(f"{where}: indented {depth - len(stack) + 1} "
                            f"level(s) deeper than its parent; treated as a "
                            f"child of the line above")
            depth = len(stack) - 1
        del stack[depth + 1:]
        parent = stack[depth]

        value = read_marker(tok, numbering_kind(depth))
        if value is None:
            warnings.append(f"{where}: marker '{tok}.' is not "
                            f"{numbering_kind(depth)} numbering, which this "
                            f"depth uses")
        else:
            running = counters.get(id(parent))
            expected = 1 if running is None else running + 1
            if value != expected:
                warnings.append(f"{where}: marker '{tok}.' out of sequence "
                                f"(expected #{expected} at this level)")
            counters[id(parent)] = value

        span, ref = parse_range(rng, where)
        node = {"title": title.strip(), "marker": f"{tok}.", "ref": ref,
                "span": span, "children": [], "page": lineno}
        if any(k["title"] == node["title"] for k in parent["children"]):
            warnings.append(f"{where}: duplicate title {node['title']!r} under "
                            f"the same parent; the YAML keeps only the last")
        parent["children"].append(node)
        stack.append(node)

    for root in tree.values():
        set_book_span(root)
    return tree


def main(source=SOURCE_TEXT, output=OUTPUT_PATH):
    tree = parse(source)
    problems = find_problems(tree)

    document = {name: to_mapping(root) for name, root in tree.items()}
    with open(output, "w", encoding="utf-8") as f:
        f.write(f"# Book outlines, from {source.name} by "
                f"src/{Path(__file__).name} -- edit that, not this.\n"
                f"# Verse ranges are chapter:verse-chapter:verse, relative "
                f"to the book.\n")
        yaml.safe_dump(document, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=10 ** 6)

    entries = sum(count(root) for root in tree.values())
    print(f"{len(tree)} books ({', '.join(tree)}), {entries} entries -> {output}")
    print(f"\n{len(warnings)} format warnings")
    for w in warnings:
        print("  ", w)
    print(f"\n{len(problems)} verse-range problems")
    for p in problems:
        node = p["node"]
        print(f"   line {node['page']}: {node['marker']} {node['title']!r} "
              f"({node['ref']}) -- {'; '.join(p['reasons'])}")


if __name__ == "__main__":
    main(*(Path(a) for a in sys.argv[1:3]))
