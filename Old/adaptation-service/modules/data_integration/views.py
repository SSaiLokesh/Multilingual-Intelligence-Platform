import uuid
from datetime import datetime, timezone

from flask import request, jsonify

from .models import DataIntegrationRequest


# --------------------------------------------------
# In-memory storage for MVP
# --------------------------------------------------

INTEGRATED_DATA = []


def generate_record_id():
    """
    Generate a unique record ID.
    """

    return f"rec_{uuid.uuid4().hex[:8]}"


def find_existing_record(data):
    """
    Check whether the supplied text already exists
    in the integrated data.

    MVP duplicate detection is based on text.
    """

    incoming_text = data.get("text")

    if not incoming_text:
        return None

    for record in INTEGRATED_DATA:

        existing_data = record.get("data", {})

        if existing_data.get("text") == incoming_text:
            return record

    return None


def integrate_data(request_id, data):
    """
    Integrate new processed data into the current
    adaptation state.

    MVP responsibilities:

    1. Validate incoming enriched data.
    2. Check whether the record already exists.
    3. Store new records.
    4. Return adaptation/storage information.

    Actual model retraining is intentionally not
    performed here.
    """

    existing_record = find_existing_record(data)

    # -----------------------------------------
    # Existing record
    # -----------------------------------------

    if existing_record is not None:

        return {
            "action": "already_exists",
            "record_id": existing_record["record_id"],
            "is_new": False,
            "version": existing_record["version"]
        }

    # -----------------------------------------
    # New record
    # -----------------------------------------

    record_id = generate_record_id()

    version = f"data-v{len(INTEGRATED_DATA) + 1}"

    record = {
        "record_id": record_id,
        "request_id": request_id,
        "data": data,
        "version": version,
        "processed_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    INTEGRATED_DATA.append(record)

    return {
        "action": "stored",
        "record_id": record_id,
        "is_new": True,
        "version": version
    }


def adapt():
    """
    Main Adaptation Service endpoint.

    Receives the complete enriched output from the
    BFF:

        text
        language
        predictions

    and integrates it into adaptation storage.
    """

    data = request.get_json(silent=True)

    # -----------------------------------------
    # Validate JSON
    # -----------------------------------------

    if not isinstance(data, dict):

        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": "Request body must be a JSON object."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    # -----------------------------------------
    # Request ID
    # -----------------------------------------

    request_id = data.get("request_id")

    if not request_id:

        return jsonify({
            "request_id": None,
            "status": "error",
            "error": {
                "code": "MISSING_REQUEST_ID",
                "message": "Field 'request_id' is required."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    # -----------------------------------------
    # Data
    # -----------------------------------------

    incoming_data = data.get("data")

    if not isinstance(incoming_data, dict):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_DATA",
                "message": "Field 'data' must be a JSON object."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    # -----------------------------------------
    # Text validation
    # -----------------------------------------

    text = incoming_data.get("text")

    if not isinstance(text, str) or not text.strip():

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_TEXT",
                "message": "Valid text is required."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    # -----------------------------------------
    # Language validation
    # -----------------------------------------

    language = incoming_data.get("language")

    if not isinstance(language, dict):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_LANGUAGE",
                "message": "Valid language information is required."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    # -----------------------------------------
    # Prediction validation
    # -----------------------------------------

    predictions = incoming_data.get("predictions")

    if not isinstance(predictions, list):

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_PREDICTIONS",
                "message": "Field 'predictions' must be a list."
            },
            "metadata": {
                "service": "adaptation-service"
            }
        }), 400

    try:

        adaptation_result = integrate_data(
            request_id=request_id,
            data=incoming_data
        )

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "adaptation": {
                "action": adaptation_result["action"],
                "record_id": adaptation_result["record_id"],
                "is_new": adaptation_result["is_new"],
                "version": adaptation_result["version"]
            },
            "metadata": {
                "service": "adaptation-service",
                "service_version": "1.0.0",
                "adaptation_stage": "data-integration"
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
                "service": "adaptation-service"
            }
        }), 500