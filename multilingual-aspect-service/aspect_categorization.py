def categorize_aspects(aspects: list, language: dict) -> list:

    categorized_aspects = []

    for aspect in aspects:

        aspect_text = aspect.get("text", "")

        category = "Other"

        if "camera" in aspect_text.lower():
            category = "Camera"

        elif "battery" in aspect_text.lower():
            category = "Battery"

        categorized_aspects.append({
            "text": aspect_text,
            "category": category
        })

    return categorized_aspects