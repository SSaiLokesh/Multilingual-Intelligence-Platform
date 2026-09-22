import re
import unicodedata


def normalize(text: str) -> str:

    if not isinstance(text, str):
        raise ValueError(
            "Text must be a string."
        )

    if not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    text = unicodedata.normalize(
        "NFKC",
        text
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = "".join(
        char
        for char in text
        if char.isprintable()
        or char in "\n\r\t"
    )

    text = re.sub(
        r"[\r\n\t]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        text
    )

    return text.strip()