def detect_language(text: str) -> dict:

    if not text:
        raise ValueError("Text cannot be empty.")

    # Temporary implementation.
    # Replace this with the actual multilingual
    # language detection model later.

    return {
        "name": "English",
        "code": "en",
        "confidence": 0.80
    }