import requests
import json

BASE_URL = "https://multilingual-intelligence-platform-6y6p.onrender.com"

url = f"{BASE_URL}/process"

payload = {
    "request_id": "req_12345678",
    "text": "The camera quality is excellent but the battery life is poor."
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response:")

    try:
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:")
    print(e)