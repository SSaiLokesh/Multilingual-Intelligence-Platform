class LanguageInfo:
    """
    Represents detected language information.
    """

    def __init__(
        self,
        name,
        code,
        confidence
    ):
        self.name = name
        self.code = code
        self.confidence = confidence

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "confidence": self.confidence
        }


class AspectInfo:
    """
    Represents an extracted aspect.
    """

    def __init__(
        self,
        text,
        category=None
    ):
        self.text = text
        self.category = category

    def to_dict(self):
        data = {
            "text": self.text
        }

        if self.category is not None:
            data["category"] = self.category

        return data