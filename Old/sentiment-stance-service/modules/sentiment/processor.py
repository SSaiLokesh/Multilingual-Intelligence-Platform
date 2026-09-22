POSITIVE_WORDS = {
    "excellent",
    "good",
    "great",
    "amazing",
    "awesome",
    "fantastic",
    "love",
    "loved",
    "best",
    "perfect",
    "nice",
    "wonderful",
    "satisfied",
    "smooth",
    "fast",
    "reliable"
}


NEGATIVE_WORDS = {
    "bad",
    "poor",
    "terrible",
    "horrible",
    "worst",
    "hate",
    "hated",
    "slow",
    "expensive",
    "problem",
    "problems",
    "issue",
    "issues",
    "disappointing",
    "disappointed",
    "broken",
    "weak"
}


def predict_sentiment(
    text,
    aspect
):
    """
    Predict sentiment for a given aspect.

    MVP implementation uses a simple keyword-based
    approach. This will later be replaced by the
    actual multilingual ML model.
    """

    text_lower = text.lower()

    positive_count = sum(
        1
        for word in POSITIVE_WORDS
        if word in text_lower
    )

    negative_count = sum(
        1
        for word in NEGATIVE_WORDS
        if word in text_lower
    )

    if positive_count > negative_count:
        label = "positive"

        confidence = min(
            0.60 + positive_count * 0.08,
            0.95
        )

    elif negative_count > positive_count:
        label = "negative"

        confidence = min(
            0.60 + negative_count * 0.08,
            0.95
        )

    else:
        label = "neutral"
        confidence = 0.60

    return {
        "label": label,
        "confidence": round(
            confidence,
            2
        )
    }
