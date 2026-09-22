from preprocessing import normalize
from language_detection import detect_language
from aspect_extraction import extract_aspects
from aspect_categorization import categorize_aspects


SERVICE_NAME = "multilingual-aspect-service"
SERVICE_VERSION = "1.0.0"


def process_pipeline(
    request_id: str,
    text: str
) -> dict:

    normalized_text = normalize(text)

    language = detect_language(
        normalized_text
    )

    aspects = extract_aspects(
        normalized_text,
        language
    )

    categorized_aspects = categorize_aspects(
        aspects,
        language
    )

    return {
        "request_id": request_id,
        "status": "success",
        "data": {
            "text": normalized_text,
            "language": language,
            "aspects": categorized_aspects
        },
        "metadata": {
            "service": SERVICE_NAME,
            "service_version": SERVICE_VERSION
        }
    }