class DataIntegrationRequest:
    """
    Represents data received for integration.
    """

    def __init__(
        self,
        request_id,
        data
    ):
        self.request_id = request_id
        self.data = data

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "data": self.data
        }


class IntegratedRecord:
    """
    Represents a record after integration.
    """

    def __init__(
        self,
        record_id,
        request_id,
        data,
        is_new,
        version
    ):
        self.record_id = record_id
        self.request_id = request_id
        self.data = data
        self.is_new = is_new
        self.version = version

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "data": self.data,
            "is_new": self.is_new,
            "version": self.version
        }