class ReplayMemoryRecord:
    """
    Represents a record maintained in the replay memory.

    The current MVP only stores the record.
    Future versions can use this memory during
    continual learning and LoRA adaptation.
    """

    def __init__(
        self,
        record_id,
        request_id,
        text,
        language,
        predictions,
        confidence
    ):
        self.record_id = record_id
        self.request_id = request_id
        self.text = text
        self.language = language
        self.predictions = predictions
        self.confidence = confidence

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "text": self.text,
            "language": self.language,
            "predictions": self.predictions,
            "confidence": self.confidence
        }