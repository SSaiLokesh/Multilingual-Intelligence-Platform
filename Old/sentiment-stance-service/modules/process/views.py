from flask import request, jsonify

from .processor import analyze_text


def analyze():
    """
    Main Service 2 endpoint.

    Receives the output of Service 1 and performs
    sentiment and stance analysis.
    """

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
                "service": "sentiment-stance-service"
            }
        }), 400

    request_id = data.get(
        "request_id"
    )

    text = data.get(
        "text"
    )

    language = data.get(
        "language"
    )

    aspects = data.get(
        "aspects"
    )

    # -----------------------------------------
    # Validate request ID
    # -----------------------------------------

    if not request_id:

        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "MISSING_REQUEST_ID",
                "message": "Field 'request_id' is required."
            },
            "metadata": {
                "service": "sentiment-stance-service"
            }
        }), 400

    # -----------------------------------------
    # Validate text
    # -----------------------------------------

    if not isinstance(
        text,
        str
    ) or not text.strip():

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Valid text is required."
            },
            "metadata": {
                "service": "sentiment-stance-service"
            }
        }), 400

    # -----------------------------------------
    # Validate language
    # -----------------------------------------

    if not isinstance(
        language,
        dict
    ):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_LANGUAGE",
                "message": "Valid language information is required."
            },
            "metadata": {
                "service": "sentiment-stance-service"
            }
        }), 400

    # -----------------------------------------
    # Validate aspects
    # -----------------------------------------

    if not isinstance(
        aspects,
        list
    ):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_ASPECTS",
                "message": "Field 'aspects' must be a list."
            },
            "metadata": {
                "service": "sentiment-stance-service"
            }
        }), 400

    try:

        predictions = analyze_text(
            text=text,
            language=language,
            aspects=aspects
        )

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "predictions": predictions,
            "metadata": {
                "service": "sentiment-stance-service",
                "service_version": "1.0.0",
                "model_version": "mvp-rule-based"
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
                "service": "sentiment-stance-service"
            }
        }), 500
