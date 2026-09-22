from flask import jsonify


def get_result(result_id):
    """
    Retrieve a single processing result.

    Persistent result storage will be implemented later.
    """

    return jsonify({
        "status": "success",
        "result_id": result_id,
        "message": "Result retrieval will be connected to storage."
    }), 200


def get_results():
    """
    Retrieve processing results.

    Persistent result storage will be implemented later.
    """

    return jsonify({
        "status": "success",
        "results": [],
        "message": "Result listing will be connected to storage."
    }), 200