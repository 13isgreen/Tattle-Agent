import json
import sys
from pathlib import Path

import requests

LIVE_URL = "https://api.tattleapp.io/surveys/api/customer-survey/submit"
PAYLOAD_PATH = Path("tpayload.json")


def main() -> None:

    try:
        payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read payload.json: {error}")
        sys.exit(1)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://lovesfeedback.com",
        "Referer": "https://lovesfeedback.com/",
    }

    try:
        response = requests.post(
            LIVE_URL,
            json=payload,
            headers=headers,
            timeout=20,
        )
    except requests.RequestException as error:
        print(f"Request failed: {error}")
        sys.exit(1)

    print(f"HTTP {response.status_code}")
    print(response.text)

    if not response.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
