class TextProcessRequest:
    """
    Represents a text processing request.
    """

    def __init__(self, text):
        self.text = text

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object.")

        text = data.get("text")

        if text is None:
            raise ValueError("Field 'text' is required.")

        if not isinstance(text, str):
            raise ValueError("Field 'text' must be a string.")

        if not text.strip():
            raise ValueError("Field 'text' cannot be empty.")

        return cls(text=text.strip())