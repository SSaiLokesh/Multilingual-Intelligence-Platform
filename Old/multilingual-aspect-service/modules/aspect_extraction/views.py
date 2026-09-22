from flask import request, jsonify


# Temporary MVP aspect vocabulary
ASPECT_KEYWORDS = {
    "camera": "Camera",
    "camera quality": "Camera",
    "battery": "Battery",
    "battery life": "Battery",
    "screen": "Display",
    "display": "Display",
    "display quality": "Display",
    "performance": "Performance",
    "speed": "Performance",
    "processor": "Performance",
    "price": "Price",
    "cost": "Price",
    "design": "Design",
    "build": "Build Quality",
    "build quality": "Build Quality",
    "software": "Software",
    "software experience": "Software",
    "audio": "Audio",
    "speaker": "Audio",
    "speakers": "Audio"
}


def extract_aspects():
    """
    Extract aspects from the supplied text.

    MVP implementation uses a keyword-based approach.
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": "Request body must be a JSON object."
            }
        }), 400

    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Valid text is required."
            }
        }), 400

    text_lower = text.lower()

    found_aspects = []

    # Sort by length so that
    # "battery life" is checked before "battery".
    keywords = sorted(
        ASPECT_KEYWORDS.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for keyword, category in keywords:

        if keyword in text_lower:

            already_exists = any(
                aspect["text"].lower() == keyword
                for aspect in found_aspects
            )

            if not already_exists:
                found_aspects.append({
                    "text": keyword,
                    "category": category
                })

    return jsonify({
        "status": "success",
        "data": {
            "aspects": found_aspects
        }
    }), 200