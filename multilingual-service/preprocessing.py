import re
import unicodedata


def normalize(text: str) -> str:

    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace line breaks and tabs with spaces
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text