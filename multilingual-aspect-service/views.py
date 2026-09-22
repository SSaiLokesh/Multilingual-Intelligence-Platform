from flask import request, jsonify
from pipeline import process_pipeline


def process_request():
    try:
        request_data = request.get_json(silent=True)

        if not request_data:
            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_JSON",
                    "message": "Request body must contain valid JSON."
                },
                "metadata": {
                    "service": "multilingual-aspect-service",
                    "service_version": "1.0.0"
                }
            }), 400

        request_id = request_data.get("request_id")
        text = request_data.get("text")

        if not request_id:
            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "MISSING_REQUEST_ID",
                    "message": "request_id is required."
                },
                "metadata": {
                    "service": "multilingual-aspect-service",
                    "service_version": "1.0.0"
                }
            }), 400

        if not text:
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "MISSING_TEXT",
                    "message": "text is required."
                },
                "metadata": {
                    "service": "multilingual-aspect-service",
                    "service_version": "1.0.0"
                }
            }), 400

        if not isinstance(text, str):
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_TEXT",
                    "message": "text must be a string."
                },
                "metadata": {
                    "service": "multilingual-aspect-service",
                    "service_version": "1.0.0"
                }
            }), 400

        result = process_pipeline(
            request_id=request_id,
            text=text
        )

        return jsonify(result), 200

    except Exception:
        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "Unable to process text."
            },
            "metadata": {
                "service": "multilingual-aspect-service",
                "service_version": "1.0.0"
            }
        }), 500