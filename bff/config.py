import os


class Config:
    """
    Application configuration for the BFF.
    """

    # Flask
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # API version
    API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

    # Service URLs
    MULTILINGUAL_ASPECT_SERVICE_URL = os.getenv(
        "MULTILINGUAL_ASPECT_SERVICE_URL",
        "http://localhost:8001"
    )

    SENTIMENT_STANCE_SERVICE_URL = os.getenv(
        "SENTIMENT_STANCE_SERVICE_URL",
        "http://localhost:8002"
    )

    ADAPTATION_SERVICE_URL = os.getenv(
        "ADAPTATION_SERVICE_URL",
        "http://localhost:8003"
    )

    # Request timeout in seconds
    SERVICE_TIMEOUT = int(
        os.getenv("SERVICE_TIMEOUT", "30")
    )