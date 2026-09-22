import requests

url = "https://multilingual-intelligence-platform-6y6p.onrender.com//adapt"

payload = {
    "request_id": "req_12345678",
    "data": {
        "text": "The camera quality is excellent but battery life is poor.",
        "language": {
            "code": "en",
            "confidence": 0.98
        },
        "predictions": [
            {
                "aspect": "camera quality",
                "category": "Camera",
                "sentiment": {
                    "label": "positive",
                    "confidence": 0.95
                },
                "stance": {
                    "target": "camera quality",
                    "label": "support",
                    "confidence": 0.91
                }
            },
            {
                "aspect": "battery life",
                "category": "Battery",
                "sentiment": {
                    "label": "negative",
                    "confidence": 0.93
                },
                "stance": {
                    "target": "battery life",
                    "label": "against",
                    "confidence": 0.87
                }
            }
        ]
    }
}

try:
    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)
    print("Response:")

    try:
        print(response.json())
    except ValueError:
        print(response.text)

except requests.exceptions.ConnectionError:
    print("Could not connect to the adaptation service.")
    print("Make sure the service is running on http://localhost:8003")