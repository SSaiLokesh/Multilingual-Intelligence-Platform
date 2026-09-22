"""
Stance Processor

Responsible for target-level stance prediction.

Labels:
    support
    against
    neutral
"""

import re


SUPPORT_WORDS = {
    "support",
    "supports",
    "supported",
    "supporting",
    "agree",
    "agrees",
    "agreed",
    "agreeing",
    "approve",
    "approves",
    "approved",
    "favor",
    "favors",
    "favored",
    "favour",
    "favourites",
    "recommend",
    "recommended",
    "recommendation",
    "yes",
    "positive",
    "beneficial",
    "benefit",
    "helpful",
    "good",
    "great",
    "excellent",
    "effective",
    "useful",
    "important",
    "necessary",
    "valuable",
}


AGAINST_WORDS = {
    "oppose",
    "opposes",
    "opposed",
    "opposing",
    "against",
    "disagree",
    "disagrees",
    "disagreed",
    "reject",
    "rejects",
    "rejected",
    "rejecting",
    "deny",
    "denies",
    "denied",
    "no",
    "negative",
    "harmful",
    "harm",
    "bad",
    "poor",
    "terrible",
    "awful",
    "useless",
    "ineffective",
    "unnecessary",
    "disappointing",
    "problem",
    "problems",
    "issue",
    "issues",
}


def _tokenize(text):
    """
    Convert text into lowercase tokens.
    """

    return re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )


def _get_target_context(text, target, window=100):
    """
    Extract context surrounding the target.
    """

    text_lower = text.lower()
    target_lower = target.lower().strip()

    position = text_lower.find(target_lower)

    if position == -1:
        return text

    start = max(
        0,
        position - window
    )

    end = min(
        len(text),
        position + len(target_lower) + window
    )

    return text[start:end]


def _calculate_stance(context):
    """
    Calculate support/against lexical scores.
    """

    tokens = _tokenize(context)

    support_score = 0
    against_score = 0

    for token in tokens:

        if token in SUPPORT_WORDS:
            support_score += 1

        elif token in AGAINST_WORDS:
            against_score += 1

    return support_score, against_score


def predict_stance(text, aspect, language):
    """
    Predict stance toward the supplied target.

    Parameters:
        text: Complete input text.
        aspect: Aspect/target object.
        language: Language information.

    Returns:
        {
            "target": "camera quality",
            "label": "support",
            "confidence": 0.91
        }
    """

    target = aspect.get("text", "")

    context = _get_target_context(
        text,
        target
    )

    support_score, against_score = _calculate_stance(
        context
    )

    total_score = support_score + against_score

    if total_score == 0:

        return {
            "target": target,
            "label": "neutral",
            "confidence": 0.60
        }

    if support_score > against_score:

        confidence = min(
            0.95,
            0.70 + (
                0.05 *
                (support_score - against_score)
            )
        )

        return {
            "target": target,
            "label": "support",
            "confidence": round(confidence, 2)
        }

    if against_score > support_score:

        confidence = min(
            0.95,
            0.70 + (
                0.05 *
                (against_score - support_score)
            )
        )

        return {
            "target": target,
            "label": "against",
            "confidence": round(confidence, 2)
        }

    return {
        "target": target,
        "label": "neutral",
        "confidence": 0.65
    }