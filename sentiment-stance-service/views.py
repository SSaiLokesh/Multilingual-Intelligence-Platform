from flask import request, jsonify

from pipeline import analyze


def analyze_view():

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body must be a JSON object."
                }
            }), 400

        request_id = data.get("request_id")
        text = data.get("text")
        language = data.get("language")
        aspects = data.get("aspects")

        if not request_id:
            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "request_id is required."
                }
            }), 400

        if not isinstance(text, str) or not text.strip():
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "text is required and must be a non-empty string."
                }
            }), 400

        if not isinstance(language, dict):
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "language is required."
                }
            }), 400

        if not isinstance(aspects, list) or not aspects:
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "aspects are required."
                }
            }), 400

        for aspect in aspects:

            if not isinstance(aspect, dict):
                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must be an object."
                    }
                }), 400

            if not aspect.get("text"):
                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must contain text."
                    }
                }), 400

            if not aspect.get("category"):
                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must contain category."
                    }
                }), 400

        predictions = analyze(
            request_id=request_id,
            text=text,
            language=language,
            aspects=aspects
        )

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "predictions": predictions
        }), 200

    except Exception:
        return jsonify({
            "request_id": data.get("request_id") if isinstance(data, dict) else None,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "An error occurred while processing the request."
            }
        }), 500


def health_view():

    return jsonify({
        "service": "sentiment-stance-service",
        "status": "healthy"
    }), 200