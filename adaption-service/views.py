from flask import request, jsonify

from pipeline import adapt

from config import (
    SERVICE_NAME,
    SERVICE_VERSION
)


def adapt_view():

    try:

        payload = request.get_json(
            silent=True
        )

        if not isinstance(payload, dict):

            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body must be a JSON object."
                }
            }), 400

        request_id = payload.get(
            "request_id"
        )

        data = payload.get(
            "data"
        )

        try:

            result = adapt(
                request_id=request_id,
                data=data
            )

        except ValueError as error:

            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": str(error)
                }
            }), 400

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "adaptation": {
                "action": result["action"],
                "record_id": result["record_id"],
                "is_new": result["is_new"]
            },
            "metadata": {
                "service": SERVICE_NAME,
                "service_version": SERVICE_VERSION
            }
        }), 200

    except Exception:

        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "An error occurred while processing the adaptation request."
            }
        }), 500


def health_view():

    return jsonify({
        "service": SERVICE_NAME,
        "status": "healthy",
        "version": SERVICE_VERSION
    }), 200