def categorize_aspects(aspects: list, language: dict) -> list:
    """
    Assign categories to extracted aspects.

    Returns:
        [
            {
                "text": "camera quality",
                "category": "Camera"
            },
            {
                "text": "battery life",
                "category": "Battery"
            }
        ]
    """