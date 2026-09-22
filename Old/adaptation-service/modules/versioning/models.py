class VersionRecord:
    """
    Represents a version of the adaptation state.
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