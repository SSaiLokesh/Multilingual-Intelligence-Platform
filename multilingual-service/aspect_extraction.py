def extract_aspects(text: str, language: dict) -> list:
    """
    Extract aspect phrases from normalized text.

    Returns:
        [
            {
                "text": "camera quality"
            },
            {
                "text": "battery life"
            }
        ]
    """