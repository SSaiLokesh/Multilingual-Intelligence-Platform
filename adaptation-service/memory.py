import json
import os

from config import MEMORY_FILE


def _ensure_storage():

    directory = os.path.dirname(MEMORY_FILE)

    if directory:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=2
            )


def _load_memory():

    _ensure_storage()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(file)

            if isinstance(memory, list):
                return memory

            return []

    except (json.JSONDecodeError, OSError):

        return []


def _save_memory(memory):

    _ensure_storage()

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=2,
            ensure_ascii=False
        )


def update_memory(record):

    memory = _load_memory()

    record_id = record.get("record_id")

    for item in memory:

        if item.get("record_id") == record_id:

            return {
                "updated": False,
                "record_id": record_id,
                "memory_size": len(memory)
            }

    memory_entry = {
        "record_id": record_id,
        "request_id": record.get("request_id"),
        "replay_eligible": True
    }

    memory.append(memory_entry)

    _save_memory(memory)

    return {
        "updated": True,
        "record_id": record_id,
        "memory_size": len(memory)
    }


def get_memory_status():

    memory = _load_memory()

    return {
        "memory_size": len(memory)
    }


def is_replay_eligible(record_id):

    memory = _load_memory()

    for item in memory:

        if item.get("record_id") == record_id:

            return bool(
                item.get(
                    "replay_eligible",
                    False
                )
            )

    return False