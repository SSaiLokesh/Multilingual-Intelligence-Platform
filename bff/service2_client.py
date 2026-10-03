import requests

from config import Config


def call_service2(request_data):
    """
    Send Service 1 output to Service 2.

    Service 2 is responsible for:
    - sentiment analysis
    - stance detection
    """

    url = f"{Config.SERVICE2_URL}/analyze"

    print("[BFF] Service 2 URL:", url)
    print("[BFF] Sending request to Service 2...")

    try:
        response = requests.post(
            url,
            json=request_data,
            timeout=Config.REQUEST_TIMEOUT
        )

        print(response)

        print(
            f"[BFF] Service 2 response received. "
            f"HTTP Status: {response.status_code}"
        )

        response.raise_for_status()

        print("[BFF] Service 2 request successful.")

        return response.json()

    except requests.exceptions.Timeout:
        print("[BFF ERROR] Service 2 request timed out.")
        raise RuntimeError("Service 2 request timed out.")

    except requests.exceptions.ConnectionError:
        print("[BFF ERROR] Unable to connect to Service 2.")
        raise RuntimeError("Unable to connect to Service 2.")

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"

        print(
            f"[BFF ERROR] Service 2 returned HTTP {status_code}."
        )

        raise RuntimeError(
            f"Service 2 returned HTTP {status_code}."
        )

    except requests.exceptions.RequestException as exc:
        print(
            f"[BFF ERROR] Service 2 request failed: {str(exc)}"
        )

        raise RuntimeError(
            f"Service 2 request failed: {str(exc)}"
        )