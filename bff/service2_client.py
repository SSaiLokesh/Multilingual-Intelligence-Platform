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

    try:
        response = requests.post(
            url,
            json=request_data,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Service 2 request timed out.")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Unable to connect to Service 2.")

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"
        raise RuntimeError(
            f"Service 2 returned HTTP {status_code}."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Service 2 request failed: {str(exc)}"
        )