from service1_client import call_service1
from service2_client import call_service2
from service3_client import call_service3


def build_service2_input(service1_result):
    """
    Build the request expected by Service 2
    using Service 1 output.
    """

    print("[BFF] Building Service 2 input...")

    if not isinstance(service1_result, dict):
        print("[BFF ERROR] Invalid response received from Service 1.")
        raise RuntimeError("Invalid response received from Service 1.")

    if service1_result.get("status") != "success":
        print("[BFF ERROR] Service 1 processing failed.")
        raise RuntimeError(
            service1_result.get(
                "message",
                "Service 1 processing failed."
            )
        )

    data = service1_result.get("data", {})

    print("[BFF] Service 2 input built successfully.")

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

    print("[BFF] Combining Service 1 and Service 2 results...")

    if not isinstance(service1_result, dict):
        print("[BFF ERROR] Invalid Service 1 result.")
        raise RuntimeError("Invalid Service 1 result.")

    if not isinstance(service2_result, dict):
        print("[BFF ERROR] Invalid Service 2 result.")
        raise RuntimeError("Invalid Service 2 result.")

    if service1_result.get("status") != "success":
        print("[BFF ERROR] Service 1 processing failed.")
        raise RuntimeError("Service 1 processing failed.")

    if service2_result.get("status") != "success":
        print("[BFF ERROR] Service 2 processing failed.")
        raise RuntimeError("Service 2 processing failed.")

    service1_data = service1_result.get("data", {})

    print("[BFF] Service 1 + Service 2 results combined successfully.")

    return {
        "text": service1_data.get("text"),
        "language": service1_data.get("language"),
        "predictions": service2_result.get("predictions", [])
    }


def build_service3_input(request_id, enriched_data):
    """
    Build the request expected by Service 3.
    """

    print(
        f"[BFF] Building Service 3 input for request_id: {request_id}"
    )

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

    print(
        f"[BFF] Building final response for request_id: {request_id}"
    )

    if not isinstance(adaptation_result, dict):
        print("[BFF ERROR] Invalid response received from Service 3.")
        raise RuntimeError(
            "Invalid response received from Service 3."
        )

    print("[BFF] Final response built successfully.")

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

    print("\n========================================")
    print("[BFF] PROCESS STARTED")
    print("========================================")

    # -------------------------------------------------
    # STEP 1 — Service 1
    # -------------------------------------------------

    print("[BFF] STEP 1: Calling Service 1...")

    service1_result = call_service1(request_data)

    print("[BFF] STEP 1: Service 1 response received.")

    request_id = service1_result.get(
        "request_id",
        request_data.get("request_id")
    )

    print(f"[BFF] Request ID: {request_id}")

    # -------------------------------------------------
    # STEP 2 — Build Service 2 request
    # -------------------------------------------------

    print("[BFF] STEP 2: Building Service 2 request...")

    service2_input = build_service2_input(
        service1_result
    )

    print("[BFF] STEP 2: Service 2 request built successfully.")

    # -------------------------------------------------
    # STEP 3 — Service 2
    # -------------------------------------------------

    print("[BFF] STEP 3: Calling Service 2...")

    service2_result = call_service2(
        service2_input
    )

    print("[BFF] STEP 3: Service 2 response received.")

    # -------------------------------------------------
    # STEP 4 — Combine Service 1 + Service 2
    # -------------------------------------------------

    print("[BFF] STEP 4: Combining Service 1 + Service 2...")

    enriched_data = build_enriched_data(
        service1_result,
        service2_result
    )

    print("[BFF] STEP 4: Enriched data created successfully.")

    # -------------------------------------------------
    # STEP 5 — Build Service 3 request
    # -------------------------------------------------

    print("[BFF] STEP 5: Building Service 3 request...")

    service3_input = build_service3_input(
        request_id,
        enriched_data
    )

    print("[BFF] STEP 5: Service 3 request built successfully.")

    # -------------------------------------------------
    # STEP 6 — Service 3
    # -------------------------------------------------

    print("[BFF] STEP 6: Calling Service 3...")

    adaptation_result = call_service3(
        service3_input
    )

    print("[BFF] STEP 6: Service 3 response received.")

    # -------------------------------------------------
    # STEP 7 — Final frontend response
    # -------------------------------------------------

    print("[BFF] STEP 7: Building final frontend response...")

    final_response = build_final_response(
        request_id,
        enriched_data,
        adaptation_result
    )

    print("[BFF] STEP 7: Final frontend response ready.")

    print("========================================")
    print("[BFF] PROCESS COMPLETED")
    print("========================================\n")

    return final_response