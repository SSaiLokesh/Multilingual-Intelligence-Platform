from flask import jsonify, request

from pipeline import process


def process_request():
    """
    Handle POST /process.
    """

    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be JSON."
        }), 400

    request_data = request.get_json()

    if not isinstance(request_data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a JSON object."
        }), 400

    request_id = request_data.get("request_id")
    text = request_data.get("text")

    if not request_id:
        return jsonify({
            "status": "error",
            "message": "Missing required field: request_id."
        }), 400

    if not text:
        return jsonify({
            "status": "error",
            "message": "Missing required field: text."
        }), 400

    if not isinstance(text, str):
        return jsonify({
            "status": "error",
            "message": "The text field must be a string."
        }), 400

    if not text.strip():
        return jsonify({
            "status": "error",
            "message": "The text field cannot be empty."
        }), 400

    try:
        result = process(request_data)

        return jsonify(result), 200

    except RuntimeError as exc:
        return jsonify({
            "request_id": request_id,
            "status": "error",
            "message": str(exc)
        }), 502

    except Exception as exc:
        return jsonify({
            "request_id": request_id,
            "status": "error",
            "message": f"Unexpected BFF error: {str(exc)}"
        }), 500


def health_check():
    """
    Handle GET /health.
    """

    return jsonify({
        "status": "success",
        "service": "bff",
        "message": "BFF is running."
    }), 200