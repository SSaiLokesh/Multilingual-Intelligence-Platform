from langdetect import detect_langs, LangDetectException


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean"
}


def detect_language(text: str) -> dict:

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        predictions = detect_langs(text)

        if not predictions:
            raise ValueError("Unable to detect language.")

        prediction = predictions[0]

        code = prediction.lang
        confidence = float(prediction.prob)

        return {
            "name": LANGUAGE_NAMES.get(code, code),
            "code": code,
            "confidence": round(confidence, 4)
        }

    except LangDetectException as exc:
        raise ValueError(
            "Language detection failed."
        ) from exc