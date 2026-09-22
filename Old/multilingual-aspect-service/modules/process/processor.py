from modules.preprocessing.processor import process_text


def process_pipeline(text):
    """
    Execute the complete Multilingual + Aspect pipeline.

    Pipeline:
        preprocessing
        -> language detection
        -> aspect extraction
        -> aspect categorization
    """

    processed_text = process_text(text)

    # -----------------------------------------
    # Language detection
    # -----------------------------------------

    language = detect_language(processed_text)

    # -----------------------------------------
    # Aspect extraction
    # -----------------------------------------

    aspects = extract_aspects(processed_text)

    # -----------------------------------------
    # Aspect categorization
    # -----------------------------------------

    aspects = categorize_aspects(aspects)

    return {
        "text": processed_text,
        "language": language,
        "aspects": aspects
    }


def detect_language(text):

    if any(
        "\u0900" <= char <= "\u097F"
        for char in text
    ):
        return {
            "name": "Hindi",
            "code": "hi",
            "confidence": 0.90
        }

    elif any(
        "\u0C00" <= char <= "\u0C7F"
        for char in text
    ):
        return {
            "name": "Telugu",
            "code": "te",
            "confidence": 0.90
        }

    elif any(
        "\u4E00" <= char <= "\u9FFF"
        for char in text
    ):
        return {
            "name": "Chinese",
            "code": "zh",
            "confidence": 0.90
        }

    elif any(
        "\u3040" <= char <= "\u30FF"
        for char in text
    ):
        return {
            "name": "Japanese",
            "code": "ja",
            "confidence": 0.90
        }

    return {
        "name": "English",
        "code": "en",
        "confidence": 0.80
    }


def extract_aspects(text):

    aspect_keywords = {
        "camera quality": "Camera",
        "camera": "Camera",
        "battery life": "Battery",
        "battery": "Battery",
        "display quality": "Display",
        "display": "Display",
        "screen": "Display",
        "performance": "Performance",
        "processor": "Performance",
        "speed": "Performance",
        "price": "Price",
        "cost": "Price",
        "design": "Design",
        "build quality": "Build Quality",
        "build": "Build Quality",
        "software": "Software",
        "speaker": "Audio",
        "speakers": "Audio",
        "audio": "Audio"
    }

    text_lower = text.lower()

    aspects = []

    for keyword, category in sorted(
        aspect_keywords.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):

        if keyword in text_lower:

            if not any(
                aspect["text"] == keyword
                for aspect in aspects
            ):
                aspects.append({
                    "text": keyword,
                    "category": category
                })

    return aspects


def categorize_aspects(aspects):

    for aspect in aspects:

        if not aspect.get("category"):
            aspect["category"] = "Other"

    return aspects