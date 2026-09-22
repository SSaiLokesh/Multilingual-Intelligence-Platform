class PredictionConfidence:
    """
    Represents a prediction label and confidence.
    """

    def __init__(
        self,
        label,
        confidence
    ):
        self.label = label
        self.confidence = confidence

    def to_dict(self):
        return {
            "label": self.label,
            "confidence": self.confidence
        }


class Prediction:
    """
    Represents the combined sentiment and stance
    prediction for an aspect.
    """

    def __init__(
        self,
        aspect,
        category,
        sentiment,
        stance
    ):
        self.aspect = aspect
        self.category = category
        self.sentiment = sentiment
        self.stance = stance

    def to_dict(self):
        return {
            "aspect": self.aspect,
            "category": self.category,
            "sentiment": self.sentiment,
            "stance": self.stance
        }
