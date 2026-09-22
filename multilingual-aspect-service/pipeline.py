from preprocessing import normalize
from language_detection import detect_language
from aspect_extraction import extract_aspects
from aspect_categorization import categorize_aspects


SERVICE_NAME = "multilingual-aspect-service"
SERVICE_VERSION = "1.0.0"


def process_pipeline(request_id: str, text: str) -> dict:

    # Stage 1: Preprocessing
    normalized_text = normalize(text)

    # Stage 2: Language Detection
    language = detect_language(normalized_text)

    # Stage 3: Aspect Extraction
    aspects = extract_aspects(
        normalized_text,
        language
    )

    # Stage 4: Aspect Categorization
    categorized_aspects = categorize_aspects(
        aspects,
        language
    )

    # Final response
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