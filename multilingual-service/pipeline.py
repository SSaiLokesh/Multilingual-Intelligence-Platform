def process_pipeline(request_id: str, text: str) -> dict:
    normalized_text = normalize(text)

    language = detect_language(normalized_text)

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
            "service": "multilingual-aspect-service",
            "service_version": "1.0.0"
        }
    }