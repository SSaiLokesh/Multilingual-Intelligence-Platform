from flask import request, jsonify


def detect_language():
    """
    Detect the language of the supplied text.

    MVP implementation uses a simple heuristic.
    This will later be replaced with a proper
    multilingual language detection model.
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

    text = text.strip()

    # -----------------------------------------
    # Simple MVP language heuristic
    # -----------------------------------------

    if any(
        "\u0900" <= char <= "\u097F"
        for char in text
    ):
        language = {
            "name": "Hindi",
            "code": "hi",
            "confidence": 0.90
        }

    elif any(
        "\u0C00" <= char <= "\u0C7F"
        for char in text
    ):
        language = {
            "name": "Telugu",
            "code": "te",
            "confidence": 0.90
        }

    elif any(
        "\u4E00" <= char <= "\u9FFF"
        for char in text
    ):
        language = {
            "name": "Chinese",
            "code": "zh",
            "confidence": 0.90
        }

    elif any(
        "\u3040" <= char <= "\u30FF"
        for char in text
    ):
        language = {
            "name": "Japanese",
            "code": "ja",
            "confidence": 0.90
        }

    else:
        language = {
            "name": "English",
            "code": "en",
            "confidence": 0.80
        }

    return jsonify({
        "status": "success",
        "data": {
            "language": language
        }
    }), 200