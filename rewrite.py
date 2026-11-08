import json
import random
import secrets
import uuid
from copy import deepcopy
from datetime import datetime
from pathlib import Path

PAYLOAD_FILE = Path("payload.json")
EMAILS_FILE = Path("test_emails_100.txt")
OUTPUT_FILE = Path("tpayload.json")


def load_payload() -> dict:
    try:
        with PAYLOAD_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise SystemExit(f"Could not find {PAYLOAD_FILE}")
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {PAYLOAD_FILE}: {error}")

def load_emails() -> list[str]:
    try:
        emails = EMAILS_FILE.read_text(encoding="utf-8").split()
    except FileNotFoundError:
        raise SystemExit(f"Could not find {EMAILS_FILE}")

    if not emails:
        raise SystemExit("The email list is empty.")

    return emails

def generate_session_id() -> str:
    # Generates 24 hexadecimal characters.
    return secrets.token_hex(12)


def generate_tracker() -> str:
    # Generates a UUID such as:
    # 46801ae9-6800-4cd8-af8c-9516c0cbac4b
    return str(uuid.uuid4())


def generate_timestamp() -> str:
    # Example:
    # 2026-08-06T13:47:00.000-04:00
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def update_payload(payload: dict, email: str) -> dict:
    updated = deepcopy(payload)

    updated["email"] = email
    updated["sessionid"] = generate_session_id()
    updated["tracker"] = generate_tracker()
    updated["dateTimeExperiencedLocal"] = generate_timestamp()
    updated["surveyTimeInSeconds"] = random.randint(45, 180)

    # Optional randomized browser dimensions.
    updated["viewportWidth"] = random.choice([1366, 1440, 1536, 1600, 1920])
    updated["viewportHeight"] = random.choice([720, 768, 864, 900, 1080])

    return updated


def main() -> None:
    base_payload = load_payload()
    emails = load_emails()

    selected_email = random.choice(emails)
    updated_payload = update_payload(base_payload, selected_email)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(updated_payload, file, indent=2)

    print(f"Created: {OUTPUT_FILE}")
    print(f"Email: {updated_payload['email']}")
    print(f"Session ID: {updated_payload['sessionid']}")
    print(f"Tracker: {updated_payload['tracker']}")
    print(f"Timestamp: {updated_payload['dateTimeExperiencedLocal']}")
    print(f"Survey time: {updated_payload['surveyTimeInSeconds']} seconds")


if __name__ == "__main__":
    main()
