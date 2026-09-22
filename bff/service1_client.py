import requests

from config import Config


def call_service1(request_data):
    """
    Send the frontend request to Service 1.

    Service 1 is responsible for:
    - text processing
    - language detection
    - aspect extraction
    """

    url = f"{Config.SERVICE1_URL}/process"

    try:
        response = requests.post(
            url,
            json=request_data,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Service 1 request timed out.")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Unable to connect to Service 1.")

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"
        raise RuntimeError(
            f"Service 1 returned HTTP {status_code}."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Service 1 request failed: {str(exc)}"
        )