class Config:
    """
    Central configuration for the BFF.
    """

    BFF_HOST = "0.0.0.0"
    BFF_PORT = 8000

    SERVICE1_URL = "http://localhost:8001"
    SERVICE2_URL = "http://localhost:8002"
    SERVICE3_URL = "http://localhost:8003"

    REQUEST_TIMEOUT = 60