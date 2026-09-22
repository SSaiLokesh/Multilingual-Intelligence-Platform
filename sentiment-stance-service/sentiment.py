"""
Sentiment Processor

Responsible for aspect-level sentiment prediction.

Labels:
    positive
    negative
    neutral
"""

import re


POSITIVE_WORDS = {
    "excellent",
    "amazing",
    "awesome",
    "good",
    "great",
    "love",
    "loved",
    "like",
    "liked",
    "best",
    "perfect",
    "wonderful",
    "fantastic",
    "super",
    "nice",
    "happy",
    "satisfied",
    "useful",
    "helpful",
    "fast",
    "clear",
    "easy",
    "beautiful",
    "reliable",
    "impressive",
    "quality",
    "recommend",
    "recommended",
}

NEGATIVE_WORDS = {
    "bad",
    "poor",
    "terrible",
    "awful",
    "worst",
    "hate",
    "hated",
    "dislike",
    "disliked",
    "horrible",
    "useless",
    "slow",
    "difficult",
    "hard",
    "disappointing",
    "disappointed",
    "problem",
    "problems",
    "issue",
    "issues",
    "expensive",
    "broken",
    "weak",
    "noisy",
    "unreliable",
    "fail",
    "failed",
    "failure",
}


NEGATION_WORDS = {
    "not",
    "never",
    "no",
    "hardly",
    "without",
}


def _tokenize(text):
    """
    Convert text into lowercase word tokens.
    """
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def _get_aspect_context(text, aspect_text, window=8):
    """
    Extract a small text window around the aspect.

    This keeps the sentiment prediction focused on the
    relevant aspect instead of the entire sentence.
    """

    text_lower = text.lower()
    aspect_lower = aspect_text.lower().strip()

    position = text_lower.find(aspect_lower)

    if position == -1:
        return text

    start = max(0, position - 100)
    end = min(
        len(text),
        position + len(aspect_lower) + 100
    )

    return text[start:end]


def _calculate_sentiment(context):
    """
    Calculate sentiment using lightweight lexical scoring.
    """

    tokens = _tokenize(context)

    positive_score = 0
    negative_score = 0

    for index, token in enumerate(tokens):

        previous_tokens = tokens[
            max(0, index - 3):index
        ]

        negated = any(
            word in NEGATION_WORDS
            for word in previous_tokens
        )

        if token in POSITIVE_WORDS:

            if negated:
                negative_score += 1
            else:
                positive_score += 1

        elif token in NEGATIVE_WORDS:

            if negated:
                positive_score += 1
            else:
                negative_score += 1

    return positive_score, negative_score


def predict_sentiment(text, aspect, language):
    """
    Predict sentiment toward the supplied aspect.

    Parameters:
        text: Complete input text.
        aspect: Aspect object containing text/category.
        language: Language information from Service 1.

    Returns:
        {
            "label": "positive",
            "confidence": 0.95
        }
    """

    aspect_text = aspect.get("text", "")

    context = _get_aspect_context(
        text,
        aspect_text
    )

    positive_score, negative_score = _calculate_sentiment(
        context
    )

    total_score = positive_score + negative_score

    if total_score == 0:

        return {
            "label": "neutral",
            "confidence": 0.60
        }

    if positive_score > negative_score:

        confidence = min(
            0.95,
            0.70 + (
                0.05 *
                (positive_score - negative_score)
            )
        )

        return {
            "label": "positive",
            "confidence": round(confidence, 2)
        }

    if negative_score > positive_score:

        confidence = min(
            0.95,
            0.70 + (
                0.05 *
                (negative_score - positive_score)
            )
        )

        return {
            "label": "negative",
            "confidence": round(confidence, 2)
        }

    return {
        "label": "neutral",
        "confidence": 0.65
    }