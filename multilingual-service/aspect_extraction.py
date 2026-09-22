def extract_aspects(text: str, language: dict) -> list:

    if not text:
        raise ValueError("Text cannot be empty.")

    # Temporary implementation.
    # Actual aspect extraction model will be added later.

    aspects = []

    text_lower = text.lower()

    if "camera" in text_lower:
        aspects.append({
            "text": "camera quality"
        })

    if "battery" in text_lower:
        aspects.append({
            "text": "battery life"
        })

    return aspects