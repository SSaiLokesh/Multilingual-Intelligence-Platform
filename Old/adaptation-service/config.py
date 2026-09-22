import os


class Config:
    """
    Configuration for the Adaptation Service.
    """

    # -----------------------------------------
    # Flask
    # -----------------------------------------

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    # -----------------------------------------
    # Service information
    # -----------------------------------------

    SERVICE_NAME = "adaptation-service"

    SERVICE_VERSION = os.getenv(
        "SERVICE_VERSION",
        "1.0.0"
    )

    # -----------------------------------------
    # API
    # -----------------------------------------

    API_PREFIX = os.getenv(
        "API_PREFIX",
        "/internal/v1"
    )

    # -----------------------------------------
    # Server
    # -----------------------------------------

    PORT = int(
        os.getenv(
            "PORT",
            "8003"
        )
    )

    # -----------------------------------------
    # MVP memory configuration
    # -----------------------------------------

    MAX_MEMORY_RECORDS = int(
        os.getenv(
            "MAX_MEMORY_RECORDS",
            "1000"
        )
    )

    # -----------------------------------------
    # Replay buffer configuration
    # -----------------------------------------

    REPLAY_BUFFER_SIZE = int(
        os.getenv(
            "REPLAY_BUFFER_SIZE",
            "500"
        )
    )