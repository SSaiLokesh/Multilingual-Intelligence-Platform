# Multilingual + Aspect Service

Independent Flask microservice responsible for multilingual text processing and aspect analysis.

## Responsibilities

- Text preprocessing
- Language detection
- Aspect extraction
- Aspect categorization

## Does Not Handle

- Sentiment analysis
- Stance detection
- Model adaptation
- BFF orchestration

## Port

8001

## Main Endpoint

POST /internal/v1/process

## Individual Endpoints

POST /internal/v1/preprocessing/process

POST /internal/v1/language/detect

POST /internal/v1/aspect/extract

POST /internal/v1/aspect/categorize

## Example Request

```json
{
    "request_id": "req_12345678",
    "text": "The camera quality is excellent but battery life is poor."
}
````

## Example Response

```json
{
    "request_id": "req_12345678",
    "status": "success",
    "data": {
        "text": "The camera quality is excellent but battery life is poor.",
        "language": {
            "name": "English",
            "code": "en",
            "confidence": 0.80
        },
        "aspects": [
            {
                "text": "camera quality",
                "category": "Camera"
            },
            {
                "text": "battery life",
                "category": "Battery"
            }
        ]
    },
    "metadata": {
        "service": "multilingual-aspect-service",
        "service_version": "1.0.0"
    }
}
```
