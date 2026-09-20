from flask import request, jsonify

from .models import ReplayMemoryRecord


# --------------------------------------------------
# MVP in-memory replay buffer
# --------------------------------------------------

REPLAY_BUFFER = []


def calculate_average_confidence(predictions):
    """
    Calculate the average prediction confidence.

    Used by the MVP to determine how confident the
    stored predictions are.
    """

    confidences = []

    for prediction in predictions:

        sentiment = prediction.get(
            "sentiment",
            {}
        )

        stance = prediction.get(
            "stance",
            {}
        )

        sentiment_confidence = sentiment.get(
            "confidence"
        )

        stance_confidence = stance.get(
            "confidence"
        )

        if isinstance(
            sentiment_confidence,
            (int, float)
        ):
            confidences.append(
                sentiment_confidence
            )

        if isinstance(
            stance_confidence,
            (int, float)
        ):
            confidences.append(
                stance_confidence
            )

    if not confidences:
        return 0.0

    return round(
        sum(confidences) / len(confidences),
        2
    )


def add_to_memory():
    """
    Add a processed record to the replay memory.

    This is the foundation for the future:

        Confidence Evaluation
              ↓
        Pseudo-labeling
              ↓
        Replay Buffer
              ↓
        LoRA Adaptation

    The current implementation only stores the
    record. It does not train a model.
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": "Request body must be a JSON object."
            }
        }), 400

    request_id = data.get("request_id")
    record_id = data.get("record_id")
    record_data = data.get("data")

    if not request_id:

        return jsonify({
            "status": "error",
            "error": {
                "code": "MISSING_REQUEST_ID",
                "message": "Field 'request_id' is required."
            }
        }), 400

    if not record_id:

        return jsonify({
            "status": "error",
            "error": {
                "code": "MISSING_RECORD_ID",
                "message": "Field 'record_id' is required."
            }
        }), 400

    if not isinstance(record_data, dict):

        return jsonify({
            "status": "error",
            "error": {
                "code": "INVALID_DATA",
                "message": "Field 'data' must be a JSON object."
            }
        }), 400

    text = record_data.get("text", "")
    language = record_data.get(
        "language",
        {}
    )
    predictions = record_data.get(
        "predictions",
        []
    )

    confidence = calculate_average_confidence(
        predictions
    )

    # -----------------------------------------
    # Prevent duplicate memory entries
    # -----------------------------------------

    for record in REPLAY_BUFFER:

        if record["record_id"] == record_id:

            return jsonify({
                "status": "success",
                "memory": {
                    "action": "already_exists",
                    "record_id": record_id,
                    "confidence": record["confidence"],
                    "buffer_size": len(REPLAY_BUFFER)
                }
            }), 200

    # -----------------------------------------
    # Create memory record
    # -----------------------------------------

    memory_record = ReplayMemoryRecord(
        record_id=record_id,
        request_id=request_id,
        text=text,
        language=language,
        predictions=predictions,
        confidence=confidence
    )

    REPLAY_BUFFER.append(
        memory_record.to_dict()
    )

    # -----------------------------------------
    # Maintain configured buffer size
    # -----------------------------------------

    max_size = 500

    while len(REPLAY_BUFFER) > max_size:
        REPLAY_BUFFER.pop(0)

    return jsonify({
        "status": "success",
        "memory": {
            "action": "stored",
            "record_id": record_id,
            "confidence": confidence,
            "buffer_size": len(REPLAY_BUFFER)
        }
    }), 200


def get_memory():
    """
    Return current replay memory information.
    """

    return jsonify({
        "status": "success",
        "memory": {
            "size": len(REPLAY_BUFFER),
            "records": REPLAY_BUFFER
        }
    }), 200


def clear_memory():
    """
    Clear the MVP replay buffer.

    This is mainly useful during development/testing.
    """

    REPLAY_BUFFER.clear()

    return jsonify({
        "status": "success",
        "memory": {
            "action": "cleared",
            "size": 0
        }
    }), 200