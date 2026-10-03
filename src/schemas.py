def generate_progressive_cloze(verses: list[str]) -> list[str]:
    """
    Returns the scaffolded and unscaffolded cloze versions of a verse block.
    Example: 
    Scaffolded: {{c1::v1}} {{c2::v2}}
    Unscaffolded: {{c1::v1}} {{c1::v2}}
    """
    scaffolded = "<br>".join([f"{{{{c{i+1}::{v}}}}}" for i, v in enumerate(verses)])
    unscaffolded = "<br>".join([f"{{{{c1::{v}}}}}" for v in verses])
    return [scaffolded, unscaffolded]

def generate_anchored_cloze(verses: list[str]) -> str:
    """
    Leaves the first and last verse visible, clozes the middle.
    Example: v1 {{c1::v2}} {{c1::v3}} v4
    """
    if len(verses) < 3:
        return "<br>".join(verses)
        
    start_anchor = verses[0]
    end_anchor = verses[-1]
    middle_clozed = "<br>".join([f"{{{{c1::{v}}}}}" for v in verses[1:-1]])
    
    return f"{start_anchor}<br>{middle_clozed}<br>{end_anchor}"

def generate_bidirectional_cards(header: str, verses: list[str]) -> tuple[str, str]:
    """
    Returns data formatted for a Basic (and reversed) Anki card.
    Front: Header
    Back: Verses combined
    """
    combined_text = "<br>".join(verses)
    return (header, combined_text)
