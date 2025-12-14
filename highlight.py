import re

def highlight_text(email_text: str, highlights: list[str]) -> str:
    """
    Returns the FULL email text with highlighted phrases wrapped in <mark>.
    """

    highlighted_text = email_text

    for phrase in highlights:
        if not phrase.strip():
            continue

        # Escape regex characters to avoid crashes
        escaped_phrase = re.escape(phrase)

        highlighted_text = re.sub(
            escaped_phrase,
            lambda m: f"<mark>{m.group(0)}</mark>",
            highlighted_text,
            flags=re.IGNORECASE
        )

    return highlighted_text
