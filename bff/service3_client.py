import requests

from config import Config


def call_service3(request_data):
    """
    Send the complete enriched result to Service 3.

    Service 3 is responsible for:
    - validation
    - duplicate checking
    - data integration
    - memory update
    - version update
    - storage
    """

    url = f"{Config.SERVICE3_URL}/adapt"

    try:
        response = requests.post(
            url,
            json=request_data,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Service 3 request timed out.")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Unable to connect to Service 3.")

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"
        raise RuntimeError(
            f"Service 3 returned HTTP {status_code}."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Service 3 request failed: {str(exc)}"
        )