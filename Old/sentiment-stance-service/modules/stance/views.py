from flask import request, jsonify

from .processor import predict_stance


def predict_stance_view():
    """
    Handle stance prediction request.
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
    target = data.get("target")

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Valid text is required."
            }
        }), 400

    if not isinstance(target, str) or not target.strip():
        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_TARGET",
                "message": "Valid target is required."
            }
        }), 400

    result = predict_stance(
        text=text,
        target=target
    )

    return jsonify({
        "status": "success",
        "data": {
            "stance": result
        }
    }), 200
