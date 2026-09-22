from flask import jsonify

from .models import VersionRecord


# In-memory version history
VERSIONS = [
    VersionRecord(
        version="adaptation-v1.0.0",
        record_count=0,
        description="Initial adaptation service state."
    )
]


def create_version(record_count, description=""):
    """
    Create and store a new adaptation version.

    Args:
        record_count (int): Number of records included in this version.
        description (str): Description of the version.

    Returns:
        VersionRecord: Newly created version record.
    """

    version_number = len(VERSIONS)

    version = VersionRecord(
        version=f"adaptation-v1.0.{version_number}",
        record_count=record_count,
        description=description
    )

    VERSIONS.append(version)

    return version


def get_current_version():
    """
    Return the latest adaptation version.
    """

    current_version = VERSIONS[-1]

    return jsonify({
        "status": "success",
        "version": current_version.to_dict()
    }), 200


def get_version_history():
    """
    Return the complete adaptation version history.
    """

    return jsonify({
        "status": "success",
        "versions": [
            version.to_dict()
            for version in VERSIONS
        ]
    }), 200