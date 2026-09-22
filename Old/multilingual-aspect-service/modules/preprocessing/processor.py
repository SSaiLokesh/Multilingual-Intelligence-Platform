import re


def process_text(text):
    """
    Perform basic text preprocessing.
    """

    processed_text = text.strip()

    processed_text = re.sub(
        r"<[^>]+>",
        " ",
        processed_text
    )

    processed_text = re.sub(
        r"\s+",
        " ",
        processed_text
    )

    return processed_text.strip()