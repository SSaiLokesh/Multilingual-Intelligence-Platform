from service1_client import call_service1
from service2_client import call_service2
from service3_client import call_service3


def build_service2_input(service1_result):
    """
    Build the request expected by Service 2
    using Service 1 output.
    """

    if not isinstance(service1_result, dict):
        raise RuntimeError("Invalid response received from Service 1.")

    if service1_result.get("status") != "success":
        raise RuntimeError(
            service1_result.get(
                "message",
                "Service 1 processing failed."
            )
        )

    data = service1_result.get("data", {})

    return {
        "request_id": service1_result.get("request_id"),
        "text": data.get("text"),
        "language": data.get("language"),
        "aspects": data.get("aspects", [])
    }


def build_enriched_data(service1_result, service2_result):
    """
    Combine Service 1 and Service 2 outputs.
    """

    if not isinstance(service1_result, dict):
        raise RuntimeError("Invalid Service 1 result.")

    if not isinstance(service2_result, dict):
        raise RuntimeError("Invalid Service 2 result.")

    if service1_result.get("status") != "success":
        raise RuntimeError("Service 1 processing failed.")

    if service2_result.get("status") != "success":
        raise RuntimeError("Service 2 processing failed.")

    service1_data = service1_result.get("data", {})

    return {
        "text": service1_data.get("text"),
        "language": service1_data.get("language"),
        "predictions": service2_result.get("predictions", [])
    }


def build_service3_input(request_id, enriched_data):
    """
    Build the request expected by Service 3.
    """

    return {
        "request_id": request_id,
        "data": enriched_data
    }


def build_final_response(
    request_id,
    enriched_data,
    adaptation_result
):
    """
    Build the final response returned to the frontend.
    """

    if not isinstance(adaptation_result, dict):
        raise RuntimeError(
            "Invalid response received from Service 3."
        )

    return {
        "request_id": request_id,
        "status": "success",
        "data": enriched_data,
        "adaptation": adaptation_result.get(
            "adaptation",
            {}
        )
    }


def process(request_data):
    """
    Main BFF orchestration pipeline.

    Flow:

    Frontend
       ↓
    Service 1
       ↓
    Service 2
       ↓
    Combine
       ↓
    Service 3
       ↓
    Frontend
    """

    # -------------------------------------------------
    # STEP 1 — Service 1
    # -------------------------------------------------

    service1_result = call_service1(request_data)

    request_id = service1_result.get(
        "request_id",
        request_data.get("request_id")
    )

    # -------------------------------------------------
    # STEP 2 — Build Service 2 request
    # -------------------------------------------------

    service2_input = build_service2_input(
        service1_result
    )

    # -------------------------------------------------
    # STEP 3 — Service 2
    # -------------------------------------------------

    service2_result = call_service2(
        service2_input
    )

    # -------------------------------------------------
    # STEP 4 — Combine Service 1 + Service 2
    # -------------------------------------------------

    enriched_data = build_enriched_data(
        service1_result,
        service2_result
    )

    # -------------------------------------------------
    # STEP 5 — Build Service 3 request
    # -------------------------------------------------

    service3_input = build_service3_input(
        request_id,
        enriched_data
    )

    # -------------------------------------------------
    # STEP 6 — Service 3
    # -------------------------------------------------

    adaptation_result = call_service3(
        service3_input
    )

    # -------------------------------------------------
    # STEP 7 — Final frontend response
    # -------------------------------------------------

    return build_final_response(
        request_id,
        enriched_data,
        adaptation_result
    )