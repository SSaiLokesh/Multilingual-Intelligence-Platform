import uuid

import requests
from flask import request, jsonify, current_app

from .models import TextProcessRequest


def generate_request_id():
    """
    Generate a unique request ID for tracing
    the request across services.
    """

    return f"req_{uuid.uuid4().hex[:8]}"


def process_text():
    """
    Process a single text through all backend services.
    """

    request_id = generate_request_id()

    try:
        data = request.get_json(silent=True)

        text_request = TextProcessRequest.from_dict(data)

    except ValueError as error:
        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": str(error)
            },
            "metadata": {
                "service": "bff"
            }
        }), 400

    text = text_request.text

    try:
        # --------------------------------------------------
        # STEP 1: Call Multilingual + Aspect Service
        # --------------------------------------------------

        service1_url = (
            current_app.config["MULTILINGUAL_ASPECT_SERVICE_URL"]
            + "/internal/v1/process"
        )

        service1_payload = {
            "request_id": request_id,
            "text": text
        }

        service1_response = requests.post(
            service1_url,
            json=service1_payload,
            timeout=current_app.config["SERVICE_TIMEOUT"]
        )

        if service1_response.status_code != 200:
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "SERVICE_1_ERROR",
                    "message": "Multilingual aspect service failed."
                },
                "details": service1_response.json()
                if service1_response.content
                else None
            }), 502

        service1_data = service1_response.json()

        # --------------------------------------------------
        # STEP 2: Call Sentiment + Stance Service
        # --------------------------------------------------

        service2_url = (
            current_app.config["SENTIMENT_STANCE_SERVICE_URL"]
            + "/internal/v1/analyze"
        )

        service2_payload = {
            "request_id": request_id,
            "text": service1_data["data"]["text"],
            "language": service1_data["data"]["language"],
            "aspects": service1_data["data"]["aspects"]
        }

        service2_response = requests.post(
            service2_url,
            json=service2_payload,
            timeout=current_app.config["SERVICE_TIMEOUT"]
        )

        if service2_response.status_code != 200:
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "SERVICE_2_ERROR",
                    "message": "Sentiment stance service failed."
                },
                "details": service2_response.json()
                if service2_response.content
                else None
            }), 502

        service2_data = service2_response.json()

        # --------------------------------------------------
        # STEP 3: Call Adaptation Service
        # --------------------------------------------------

        service3_url = (
            current_app.config["ADAPTATION_SERVICE_URL"]
            + "/internal/v1/adapt"
        )

        service3_payload = {
            "request_id": request_id,
            "data": {
                "text": service1_data["data"]["text"],
                "language": service1_data["data"]["language"],
                "predictions": service2_data["predictions"]
            }
        }

        service3_response = requests.post(
            service3_url,
            json=service3_payload,
            timeout=current_app.config["SERVICE_TIMEOUT"]
        )

        if service3_response.status_code != 200:
            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "SERVICE_3_ERROR",
                    "message": "Adaptation service failed."
                },
                "details": service3_response.json()
                if service3_response.content
                else None
            }), 502

        service3_data = service3_response.json()

        # --------------------------------------------------
        # STEP 4: Aggregate final response
        # --------------------------------------------------

        final_response = {
            "request_id": request_id,
            "status": "success",
            "data": {
                "text": service1_data["data"]["text"],
                "language": service1_data["data"]["language"],
                "predictions": service2_data["predictions"]
            },
            "processing": {
                "adaptation_status": service3_data[
                    "adaptation"
                ]["action"]
            }
        }

        return jsonify(final_response), 200

    except requests.exceptions.Timeout:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "SERVICE_TIMEOUT",
                "message": "One of the backend services timed out."
            }
        }), 504

    except requests.exceptions.ConnectionError:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "SERVICE_UNAVAILABLE",
                "message": "Unable to connect to a backend service."
            }
        }), 503

    except Exception as error:

        return jsonify({
            "request_id": request_id,
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(error)
            }
        }), 500


def process_dataset():
    """
    Dataset processing endpoint.

    Dataset processing will be implemented after
    the text-processing pipeline is completed.
    """

    request_id = generate_request_id()

    return jsonify({
        "request_id": request_id,
        "status": "success",
        "message": "Dataset processing endpoint is available.",
        "data": {
            "status": "not_implemented"
        }
    }), 200