"""
Base model definitions.

This module is intentionally lightweight.

Future trained/pre-trained models can be loaded here
without changing the external API or pipeline structure.
"""


class BasePredictionModel:

    def __init__(self, name="lightweight-model"):
        self.name = name

    def predict(self, text):
        raise NotImplementedError(
            "Subclasses must implement predict()."
        )