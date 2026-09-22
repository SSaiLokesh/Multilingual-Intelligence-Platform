from sentiment import predict_sentiment
from stance import predict_stance


def analyze(request_id, text, language, aspects):

    predictions = []

    for aspect in aspects:

        sentiment_result = predict_sentiment(
            text=text,
            aspect=aspect,
            language=language
        )

        stance_result = predict_stance(
            text=text,
            aspect=aspect,
            language=language
        )

        predictions.append({
            "aspect": aspect["text"],
            "category": aspect["category"],
            "sentiment": sentiment_result,
            "stance": stance_result
        })

    return predictions