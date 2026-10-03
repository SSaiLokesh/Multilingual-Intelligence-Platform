from flask import request, jsonify

from pipeline import analyze


def analyze_view():

    print("\n========================================")
    print("[SERVICE 2] ANALYZE REQUEST RECEIVED")
    print("========================================")

    try:
        print("[SERVICE 2] Reading request JSON...")

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            print("[SERVICE 2 ERROR] Request body is not a JSON object.")

            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body must be a JSON object."
                }
            }), 400

        print("[SERVICE 2] Request JSON received successfully.")

        request_id = data.get("request_id")
        text = data.get("text")
        language = data.get("language")
        aspects = data.get("aspects")

        print(f"[SERVICE 2] Request ID: {request_id}")
        print("[SERVICE 2] Validating request...")

        if not request_id:
            print("[SERVICE 2 ERROR] request_id is missing.")

            return jsonify({
                "request_id": None,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "request_id is required."
                }
            }), 400

        if not isinstance(text, str) or not text.strip():
            print("[SERVICE 2 ERROR] text is missing or invalid.")

            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "text is required and must be a non-empty string."
                }
            }), 400

        if not isinstance(language, dict):
            print("[SERVICE 2 ERROR] language is missing or invalid.")

            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "language is required."
                }
            }), 400

        if not isinstance(aspects, list) or not aspects:
            print("[SERVICE 2 ERROR] aspects are missing or invalid.")

            return jsonify({
                "request_id": request_id,
                "status": "error",
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "aspects are required."
                }
            }), 400

        print(f"[SERVICE 2] Number of aspects received: {len(aspects)}")

        for aspect in aspects:

            print("[SERVICE 2] Validating aspect...")

            if not isinstance(aspect, dict):
                print("[SERVICE 2 ERROR] Aspect is not an object.")

                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must be an object."
                    }
                }), 400

            if not aspect.get("text"):
                print("[SERVICE 2 ERROR] Aspect text is missing.")

                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must contain text."
                    }
                }), 400

            if not aspect.get("category"):
                print("[SERVICE 2 ERROR] Aspect category is missing.")

                return jsonify({
                    "request_id": request_id,
                    "status": "error",
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": "Each aspect must contain category."
                    }
                }), 400

        print("[SERVICE 2] Request validation successful.")
        print("[SERVICE 2] Starting sentiment and stance analysis...")

        predictions = analyze(
            request_id=request_id,
            text=text,
            language=language,
            aspects=aspects
        )

        print("[SERVICE 2] Analysis completed successfully.")
        print(f"[SERVICE 2] Predictions generated: {len(predictions)}")
        print("[SERVICE 2] Sending response to BFF...")

        return jsonify({
            "request_id": request_id,
            "status": "success",
            "predictions": predictions
        }), 200

    except Exception:
        print("[SERVICE 2 ERROR] Processing exception occurred.")

        return jsonify({
            "request_id": data.get("request_id") if isinstance(data, dict) else None,
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "An error occurred while processing the request."
            }
        }), 500


def health_view():

    print("[SERVICE 2] Health check requested.")

    return jsonify({
        "service": "sentiment-stance-service",
        "status": "healthy"
    }), 200