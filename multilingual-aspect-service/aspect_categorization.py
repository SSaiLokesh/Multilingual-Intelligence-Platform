CATEGORY_KEYWORDS = {

    "Camera": {
        "camera",
        "cameras",
        "photo",
        "photos",
        "image",
        "images",
        "lens"
    },

    "Battery": {
        "battery",
        "charging",
        "charger"
    },

    "Display": {
        "display",
        "screen",
        "brightness",
        "resolution"
    },

    "Performance": {
        "performance",
        "processor",
        "speed",
        "ram",
        "memory"
    },

    "Audio": {
        "audio",
        "speaker",
        "speakers",
        "sound",
        "microphone"
    },

    "Design": {
        "design",
        "body",
        "build",
        "appearance"
    }
}


def categorize_aspects(
    aspects: list,
    language: dict
) -> list:

    results = []

    for aspect in aspects:

        aspect_text = aspect.get(
            "text",
            ""
        ).strip()

        words = {
            word.lower()
            for word in aspect_text.split()
        }

        category = "Other"

        for category_name, keywords in CATEGORY_KEYWORDS.items():

            if words.intersection(keywords):

                category = category_name
                break

        results.append({
            "text": aspect_text,
            "category": category
        })

    return results