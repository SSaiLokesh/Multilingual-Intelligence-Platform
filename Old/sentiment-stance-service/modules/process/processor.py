from modules.sentiment.processor import predict_sentiment
from modules.stance.processor import predict_stance


def analyze_text(
    text,
    language,
    aspects
):
    """
    Execute sentiment and stance prediction
    for all supplied aspects.
    """

    predictions = []

    for aspect_data in aspects:

        aspect_text = aspect_data.get(
            "text",
            ""
        )

        category = aspect_data.get(
            "category",
            "Other"
        )

        if not aspect_text:
            continue

        # -----------------------------------------
        # Sentiment prediction
        # -----------------------------------------

        sentiment = predict_sentiment(
            text=text,
            aspect=aspect_text
        )

        # -----------------------------------------
        # Stance prediction
        # -----------------------------------------

        stance = predict_stance(
            text=text,
            target=aspect_text
        )

        # -----------------------------------------
        # Combined prediction
        # -----------------------------------------

        predictions.append({
            "aspect": aspect_text,
            "category": category,
            "sentiment": sentiment,
            "stance": stance
        })

    return predictions
