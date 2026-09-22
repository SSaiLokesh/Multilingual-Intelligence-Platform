from flask import request, jsonify

from pipeline import process_pipeline


SERVICE_NAME = "multilingual-aspect-service"
SERVICE_VERSION = "1.0.0"


def process_request():

    request_data = request.get_json(
        silent=True
    )

    if not request_data:

        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "INVALID_JSON",
                "message": "Request body must contain valid JSON."
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
            }
        }), 400

    if not text:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "MISSING_TEXT",
                "message": "text is required."
            }
        }), 400

    if not isinstance(text, str):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "text must be a string."
            }
        }), 400

    try:

        result = process_pipeline(
            request_id=request_id,
            text=text
        )

        return jsonify(result), 200

    except Exception:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "Unable to process text."
            },
            "metadata": {
                "service": SERVICE_NAME,
                "service_version": SERVICE_VERSION
            }
        }), 500