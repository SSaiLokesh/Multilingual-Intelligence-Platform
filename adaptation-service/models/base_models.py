class AdaptationRequest:
    """
    Represents an adaptation request received from the BFF.
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


class AdaptationRecord:
    """
    Represents a processed record stored by the
    adaptation service.
    """

    def __init__(
        self,
        record_id,
        request_id,
        data,
        version
    ):
        self.record_id = record_id
        self.request_id = request_id
        self.data = data
        self.version = version

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "data": self.data,
            "version": self.version
        }


class MemoryRecord:
    """
    Represents a record maintained in adaptation memory.
    """

    def __init__(
        self,
        record_id,
        request_id,
        data,
        confidence
    ):
        self.record_id = record_id
        self.request_id = request_id
        self.data = data
        self.confidence = confidence

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "data": self.data,
            "confidence": self.confidence
        }


class VersionInfo:
    """
    Represents an adaptation/data version.
    """

    def __init__(
        self,
        version,
        record_count,
        description
    ):
        self.version = version
        self.record_count = record_count
        self.description = description

    def to_dict(self):
        return {
            "version": self.version,
            "record_count": self.record_count,
            "description": self.description
        }