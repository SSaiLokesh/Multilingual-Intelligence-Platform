
from flask import request, jsonify

from .processor import process_text


def preprocess_text():

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

    if text is None:
        return jsonify({
            "status": "error",
            "error": {
                "code": "MISSING_TEXT",
                "message": "Field 'text' is required."
            }
        }), 400

    if not isinstance(text, str):
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Field 'text' must be a string."
            }
        }), 400

    if not text.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "EMPTY_TEXT",
                "message": "Text cannot be empty."
            }
        }), 400

    processed_text = process_text(text)

    return jsonify({
        "status": "success",
        "data": {
            "original_text": text,
            "processed_text": processed_text
        }
    }), 200