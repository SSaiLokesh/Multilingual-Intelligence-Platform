from flask import request, jsonify

from .processor import process_pipeline


def process():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": "Request body must be a JSON object."
            },
            "metadata": {
                "service": "multilingual-aspect-service"
            }
        }), 400

    request_id = data.get("request_id")

    text = data.get("text")

    if not request_id:
        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "MISSING_REQUEST_ID",
                "message": "Field 'request_id' is required."
            }
        }), 400

    if not isinstance(text, str):
        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Field 'text' must be a string."
            },
            "metadata": {
                "service": "multilingual-aspect-service"
            }
        }), 400

    if not text.strip():
        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "EMPTY_TEXT",
                "message": "Text cannot be empty."
            },
            "metadata": {
                "service": "multilingual-aspect-service"
            }
        }), 400

    try:

        result = process_pipeline(text)

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "data": result,
            "metadata": {
                "service": "multilingual-aspect-service",
                "service_version": "1.0.0"
            }
        }), 200

    except Exception as error:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": str(error)
            },
            "metadata": {
                "service": "multilingual-aspect-service"
            }
        }), 500