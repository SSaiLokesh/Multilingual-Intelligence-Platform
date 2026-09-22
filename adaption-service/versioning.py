import json
import os

from config import VERSION_FILE


DEFAULT_VERSION = {
    "dataset_version": 1,
    "adaptation_version": 1,
    "record_count": 0
}


def _ensure_storage():

    directory = os.path.dirname(VERSION_FILE)

    if directory:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(VERSION_FILE):

        with open(
            VERSION_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                DEFAULT_VERSION,
                file,
                indent=2
            )


def get_current_version():

    _ensure_storage()

    try:

        with open(
            VERSION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            version = json.load(file)

            if isinstance(version, dict):
                return version

            return DEFAULT_VERSION.copy()

    except (json.JSONDecodeError, OSError):

        return DEFAULT_VERSION.copy()


def _save_version(version):

    _ensure_storage()

    with open(
        VERSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            version,
            file,
            indent=2
        )


def update_version(is_new_record):

    version = get_current_version()

    if is_new_record:

        version["record_count"] = (
            version.get("record_count", 0) + 1
        )

        version["dataset_version"] = (
            version.get("dataset_version", 1) + 1
        )

    _save_version(version)

    return version


def create_version():

    version = get_current_version()

    version["adaptation_version"] = (
        version.get("adaptation_version", 1) + 1
    )

    _save_version(version)

    return version