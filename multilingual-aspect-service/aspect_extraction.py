import spacy


# Pre-trained lightweight English model
nlp = spacy.load("en_core_web_sm")


DETERMINERS = {
    "the",
    "a",
    "an"
}


def clean_aspect(text: str) -> str:

    words = text.split()

    while words and words[0].lower() in DETERMINERS:
        words.pop(0)

    return " ".join(words).strip()


def extract_aspects(text: str, language: dict) -> list:

    if not text:
        return []

    language_code = language.get("code")

    # Current pretrained extraction pipeline
    # supports English.
    if language_code != "en":
        return []

    doc = nlp(text)

    aspects = []
    seen = set()

    for chunk in doc.noun_chunks:

        aspect = clean_aspect(chunk.text)

        if not aspect:
            continue

        key = aspect.lower()

        if key in seen:
            continue

        seen.add(key)

        aspects.append({
            "text": aspect
        })

    return aspects