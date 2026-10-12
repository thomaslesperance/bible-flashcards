"""
HTML building blocks for v2 cards (notes/sequence_v2_draft.md §8). Styles live in
assets/card.css, the type-mode script in assets/card.js.

Words come from chapter.Line.words, whose offsets leave quotes, commas and dashes
outside the word. A hidden word keeps its real text inside a span whose glyphs
CSS makes invisible or blurs, so a blank is exactly as wide as its word and a
passage has the same shape on every card. The back adds class "rv" to reveal
in place.
"""

from html import escape

from ..chapter import Line, Verse
from ..refs import VerseRef
from .tree import Node, Unit, fmt_range

# --------------------------------------------------------------------------
# Passages
# --------------------------------------------------------------------------

def _word(text: str, mode: str, rv: str) -> str:
    if mode == "blank":  # Missing words: the word's own width, glyphs invisible
        return f'<span class="mw{rv}">{escape(text)}</span>'
    if mode == "first":  # First letters: first letter, the rest blurred in place
        rest = f'<span class="bl{rv}">{escape(text[1:])}</span>' if len(text) > 1 else ""
        return escape(text[0]) + rest
    return escape(text)


def _line_html(line: Line, mode_of, start: int, rv: str) -> tuple[str, int]:
    """One line's HTML; mode_of(i) gives each word's mode. Returns (html, next word index)."""
    words, i = line.words, start
    if not words:
        return escape(line.text), i
    if mode_of(i) == "type":
        # Each word span runs to the next word, so its punctuation appears with it.
        out = []
        for k, w in enumerate(words):
            a = 0 if k == 0 else w.start
            b = words[k + 1].start if k + 1 < len(words) else len(line.text)
            head, tail = line.text[a:w.start], line.text[w.start + 1:b]
            out.append(f'<span class="tw" data-k="{escape(w.text[0].lower())}">{escape(head)}'
                       f'<span class="tw-f">{escape(w.text[0])}</span>{escape(tail)}</span>')
        return "".join(out), i + len(words)
    out, pos = [], 0
    for w in words:
        out.append(escape(line.text[pos:w.start]))
        out.append(_word(w.text, mode_of(i), rv))
        pos, i = w.end, i + 1
    out.append(escape(line.text[pos:]))
    return "".join(out), i


def passage(verses: list[Verse], breaks: set[VerseRef], word_mode=None, verse_mode=None,
            reveal: bool = False, headings: dict | None = None) -> str:
    """
    word_mode(i) -> 'show' | 'blank' | 'first' | 'type', where i counts the passage's
    words from 0. verse_mode(verse) -> 'show' | 'block' | 'dim' overrides it for a
    whole verse ('block' blurs it). headings: {VerseRef: title} drawn above a verse.
    """
    rv = " rv" if reveal else ""
    out, i = ['<div class="passage">'], 0
    for n, v in enumerate(verses):
        vmode = verse_mode(v) if verse_mode else "show"
        if headings and v.ref in headings:
            out.append(f'<div class="ph">{escape(headings[v.ref])}</div>')
        for li, line in enumerate(v.lines):
            classes = [f"ln i{line.indent}"]
            if li == 0 and n > 0 and v.ref in breaks:
                classes.append("st")  # paragraph break: a little space above
            if vmode == "dim":
                classes.append("dim")
            num = f'<sup class="vn">{v.ref.verse}</sup>' if li == 0 else ""
            if vmode == "block":
                body = f'<span class="bk{rv}">{escape(line.text)}</span>'
                i += len(line.words)
            elif vmode == "dim" or not word_mode:
                body = escape(line.text)
                i += len(line.words)
            else:
                body, i = _line_html(line, word_mode, i, rv)
            out.append(f'<div class="{" ".join(classes)}">{num}{body}</div>')
    out.append("</div>")
    return "\n".join(out)


def gap_box(label: str, inner: str) -> str:
    return f'<div class="gap"><div class="gap-l">{escape(label)}</div>{inner}</div>'


def first_line(verses: list[Verse], max_words: int = 9) -> str:
    """Opening words of a passage: its first line, cut at max_words."""
    line = verses[0].lines[0]
    words = line.words
    if len(words) <= max_words:
        return line.text
    return line.text[:words[max_words - 1].end] + " …"


# --------------------------------------------------------------------------
# Outline map (Phase 1 cards and the backs of Text -> header)
# --------------------------------------------------------------------------

def outline_map(root: Node, focus: Node | None = None, *, blank: Node | None = None,
                highlight=(), hide_parts: Node | None = None, hidden_label: str | None = None,
                expand_under: Node | None = None, reveal: bool = False,
                unit: Unit | None = None) -> str:
    """
    The outline drawn around `focus`: the path from the top down to it, every
    sibling at each level, and other branches collapsed to one line (▸ n).
    - blank: this header's title is hidden (Outline cloze).
    - hide_parts: this section's parts are collapsed into one placeholder (List the
      parts, Whole outline); hidden_label replaces the placeholder's text.
    - expand_under: draw every header under this one (Whole outline backs).
    - reveal: the back -- blanks and hidden parts are shown, highlighted.
    - unit: mark which part of a split leaf is meant.
    """
    path = set(focus.path) if focus else {root}
    if expand_under:
        path |= set(expand_under.walk())
    highlight = set(highlight)
    rows = ['<div class="omap">']

    def row(node: Node):
        classes = [f"om d{node.depth}"]
        if node in highlight or (reveal and node is blank):
            classes.append("hl")
        title = escape(node.title)
        if node is blank:
            # Fixed width, no text: the blank's length shouldn't hint at the answer.
            title = f'<span class="ans">{title}</span>' if reveal else '<span class="blank"></span>'
        if unit and unit.node is node and unit.count > 1:
            title += f' <span class="om-part">part {unit.index + 1} of {unit.count}</span>'
        expanded = node in path or node is hide_parts
        more = f'<span class="om-more">▸ {len(node.children)}</span>' if node.children and not expanded else ""
        rows.append(f'<div class="{" ".join(classes)}"><span class="om-lb">{node.label}</span>'
                    f'<span class="om-t">{title}</span><span class="om-r">{node.ref}</span>{more}</div>')
        if not node.children or not expanded:
            return
        if node is hide_parts and not reveal:
            label = hidden_label or f"{len(node.children)} parts — list them in order"
            rows.append(f'<div class="om d{node.depth + 1} hidden-parts">'
                        f'<span class="om-t">{escape(label)}</span></div>')
            return
        for c in node.children:
            row(c)

    row(root)
    rows.append("</div>")
    return "\n".join(rows)


def map_strip(root: Node, item) -> str:
    """
    Compact map for text cards: the path on one line, then the current header's
    siblings with the current one marked. `item` is a Unit or a Node.
    """
    node = item.node if isinstance(item, Unit) else item
    parent = node.parent
    crumbs = " › ".join(escape(n.title) for n in (parent.path if parent else [root]))
    sibs = []
    for s in (parent.children if parent else [node]):
        label = escape(s.title)
        if s is node:
            if isinstance(item, Unit) and item.count > 1:
                label += f" ({item.index + 1} of {item.count})"
            sibs.append(f'<span class="sb cur">● {label}</span>')
        else:
            sibs.append(f'<span class="sb">○ {label}</span>')
    return (f'<div class="strip"><div class="crumbs">{crumbs}</div>'
            f'<div class="sibs">{"".join(sibs)}</div></div>')


# --------------------------------------------------------------------------
# Card frame
# --------------------------------------------------------------------------

RUBRIC = """<table class="rubric">
<tr><td>Again</td><td>got stuck, looked, used the hint, or left out a phrase</td></tr>
<tr><td>Hard</td><td>all there, but long pauses or several small slips</td></tr>
<tr><td>Good</td><td>all there, at most one small slip</td></tr>
<tr><td>Easy</td><td>instant and word-perfect</td></tr>
</table>"""

RUBRIC_SCAFFOLD = RUBRIC.replace(
    "</table>", '<tr><td colspan="2" class="note">Scaffold card: press Easy whenever it felt effortless.</td></tr></table>')

RUBRIC_READ = '<div class="rubric note">Reading card — press <b>Easy</b>.</div>'


def frame(stage: str, banner: str, body: str, *, sub: str = "") -> str:
    """stage: read | outline | ladder | section (sets the banner colour)."""
    sub_html = f'<div class="sub">{sub}</div>' if sub else ""
    return f'<div class="v2 st-{stage}"><div class="banner">{banner}</div>{sub_html}{body}</div>'


def verses_label(verses: list[Verse]) -> str:
    n = len(verses)
    return f"{fmt_range(verses)} · {n} verse{'s' if n != 1 else ''}"
