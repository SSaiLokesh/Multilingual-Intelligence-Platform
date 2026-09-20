from flask import request, jsonify

from .processor import predict_sentiment


def predict_sentiment_view():
    """
    Handle sentiment prediction request.
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
    aspect = data.get("aspect")

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Valid text is required."
            }
        }), 400

    if not isinstance(aspect, str) or not aspect.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_ASPECT",
                "message": "Valid aspect is required."
            }
        }), 400

    result = predict_sentiment(
        text=text,
        aspect=aspect
    )

    return jsonify({
        "status": "success",
        "data": {
            "aspect": aspect,
            "sentiment": result
        }
    }), 200
