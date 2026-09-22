from flask import request, jsonify


CATEGORY_MAPPING = {
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
    "audio": "Audio",
    "speaker": "Audio",
    "speakers": "Audio"
}


def categorize_aspects():
    """
    Categorize extracted aspects.
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

    aspects = data.get("aspects")

    if not isinstance(aspects, list):
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_ASPECTS",
                "message": "Field 'aspects' must be a list."
            }
        }), 400

    categorized_aspects = []

    for aspect in aspects:

        if isinstance(aspect, str):
            aspect_text = aspect.strip()

        elif isinstance(aspect, dict):
            aspect_text = aspect.get("text", "").strip()

        else:
            continue

        if not aspect_text:
            continue

        category = CATEGORY_MAPPING.get(
            aspect_text.lower(),
            "Other"
        )

        categorized_aspects.append({
            "text": aspect_text,
            "category": category
        })

    return jsonify({
        "status": "success",
        "data": {
            "aspects": categorized_aspects
        }
    }), 200