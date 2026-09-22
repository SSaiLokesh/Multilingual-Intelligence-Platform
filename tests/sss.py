import requests

url = "http://localhost:8002/analyze"
url = "https://multilingual-intelligence-platform-chsm.onrender.com/analyze"

payload = {
    "request_id": "req_12345678",
    "text": "The camera quality is excellent but battery life is poor.",
    "language": {
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
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())