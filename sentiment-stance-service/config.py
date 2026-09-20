import os


class Config:
    """
    Configuration for the Sentiment + Stance Service.
    """

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    SERVICE_NAME = "sentiment-stance-service"

    SERVICE_VERSION = os.getenv(
        "SERVICE_VERSION",
        "1.0.0"
    )

    API_PREFIX = os.getenv(
        "API_PREFIX",
        "/internal/v1"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "8002"
        )
    )
