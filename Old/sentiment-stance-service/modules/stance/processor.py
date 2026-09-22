SUPPORT_WORDS = {
    "support",
    "supports",
    "supported",
    "agree",
    "agrees",
    "agreed",
    "approve",
    "approves",
    "approved",
    "beneficial",
    "useful",
    "helpful",
    "good",
    "great",
    "excellent",
    "positive"
}


AGAINST_WORDS = {
    "against",
    "oppose",
    "opposes",
    "opposed",
    "disagree",
    "disagrees",
    "disagreed",
    "reject",
    "rejects",
    "rejected",
    "bad",
    "poor",
    "harmful",
    "useless",
    "negative"
}


def predict_stance(
    text,
    target
):
    """
    Predict stance toward a target.

    MVP implementation uses a keyword-based approach.

    Later this will be replaced by a proper stance
    detection model.
    """

    text_lower = text.lower()

    support_count = sum(
        1
        for word in SUPPORT_WORDS
        if word in text_lower
    )

    against_count = sum(
        1
        for word in AGAINST_WORDS
        if word in text_lower
    )

    if support_count > against_count:

        label = "support"

        confidence = min(
            0.60 + support_count * 0.08,
            0.95
        )

    elif against_count > support_count:

        label = "against"

        confidence = min(
            0.60 + against_count * 0.08,
            0.95
        )

    else:

        label = "neutral"
        confidence = 0.60

    return {
        "target": target,
        "label": label,
        "confidence": round(
            confidence,
            2
        )
    }
