from data_integration import (
    validate_record,
    integrate_record
)

from memory import update_memory

from versioning import (
    update_version,
    get_current_version
)


def adapt(request_id, data):

    valid, error_message = validate_record(
        request_id,
        data
    )

    if not valid:

        raise ValueError(error_message)

    integration_result = integrate_record(
        request_id,
        data
    )

    record = integration_result["record"]

    if integration_result["is_new"]:

        memory_result = update_memory(record)

        version_result = update_version(
            is_new_record=True
        )

    else:

        memory_result = {
            "updated": False,
            "record_id": integration_result["record_id"],
            "memory_size": 0
        }

        version_result = get_current_version()

    return {
        "action": integration_result["action"],
        "record_id": integration_result["record_id"],
        "is_new": integration_result["is_new"],
        "memory": memory_result,
        "version": version_result
    }