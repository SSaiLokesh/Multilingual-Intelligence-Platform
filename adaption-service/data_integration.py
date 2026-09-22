import json
import os
import uuid

from config import RECORDS_FILE


def _ensure_storage():

    directory = os.path.dirname(RECORDS_FILE)

    if directory:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(RECORDS_FILE):

        with open(
            RECORDS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump([], file, indent=2)


def _load_records():

    _ensure_storage()

    try:

        with open(
            RECORDS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            records = json.load(file)

            if isinstance(records, list):
                return records

            return []

    except (json.JSONDecodeError, OSError):

        return []


def _save_records(records):

    _ensure_storage()

    with open(
        RECORDS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False
        )


def validate_record(request_id, data):

    if not request_id:
        return False, "request_id is required."

    if not isinstance(data, dict):
        return False, "data must be an object."

    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return False, "data.text is required."

    language = data.get("language")

    if not isinstance(language, dict):
        return False, "data.language is required."

    if not language.get("code"):
        return False, "data.language.code is required."

    predictions = data.get("predictions")

    if not isinstance(predictions, list):
        return False, "data.predictions must be a list."

    return True, None


def find_existing_record(request_id):

    records = _load_records()

    for record in records:

        if record.get("request_id") == request_id:

            return record

    return None


def create_record(request_id, data):

    records = _load_records()

    record_id = "rec_" + uuid.uuid4().hex[:12]

    record = {
        "record_id": record_id,
        "request_id": request_id,
        "data": data
    }

    records.append(record)

    _save_records(records)

    return record


def integrate_record(request_id, data):

    existing_record = find_existing_record(request_id)

    if existing_record:

        return {
            "action": "already_exists",
            "record_id": existing_record["record_id"],
            "is_new": False,
            "record": existing_record
        }

    new_record = create_record(
        request_id,
        data
    )

    return {
        "action": "stored",
        "record_id": new_record["record_id"],
        "is_new": True,
        "record": new_record
    }