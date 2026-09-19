import re

def clean_input_text(text: str) -> str:
    """Validates and cleans input text before passing to ML models."""
    if not isinstance(text, str) or not text.strip():
        return ""
    # Strip URLs and HTML tags
    text = re.sub(r'http\S+|www\S+|<[^>]*>', '', text)
    # Normalize extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text