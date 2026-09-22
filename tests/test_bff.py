import requests
import json


BFF_URL = "http://localhost:8000/process"


def test_bff():
    payload = {
        "request_id": "integration_test_001",
        "text": "The movie is good."
    }

    print("=" * 60)
    print("BFF INTEGRATION TEST")
    print("=" * 60)

    print("\nSending request to BFF...")
    print(f"URL: {BFF_URL}")

    print("\nRequest:")
    print(json.dumps(payload, indent=4))

    try:
        response = requests.post(
            BFF_URL,
            json=payload,
            timeout=60
        )

        print("\n" + "=" * 60)
        print("BFF RESPONSE")
        print("=" * 60)

        print(f"\nHTTP Status Code: {response.status_code}")

        try:
            response_data = response.json()

            print("\nResponse:")
            print(json.dumps(response_data, indent=4))

        except ValueError:
            print("\nResponse is not valid JSON:")
            print(response.text)

        if response.ok:
            print("\n" + "=" * 60)
            print("TEST RESULT: SUCCESS")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("TEST RESULT: FAILED")
            print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 60)
        print("TEST RESULT: FAILED")
        print("=" * 60)
        print("\nCould not connect to BFF.")
        print("Make sure BFF is running on:")
        print("http://localhost:8000")

    except requests.exceptions.Timeout:
        print("\n" + "=" * 60)
        print("TEST RESULT: FAILED")
        print("=" * 60)
        print("\nBFF request timed out.")

    except requests.exceptions.RequestException as error:
        print("\n" + "=" * 60)
        print("TEST RESULT: FAILED")
        print("=" * 60)
        print(f"\nRequest error: {error}")


if __name__ == "__main__":
    test_bff()