import json
import random
import subprocess
import time
from datetime import datetime, timedelta


CONFIG = "config.json"


def load_config():
    with open(CONFIG, "r") as f:
        return json.load(f)


def run_job():
    print(f"[{datetime.now()}] Running rewrite.py")

    result = subprocess.run(["python3", "rewrite.py"])

    if result.returncode == 0:
        print(f"[{datetime.now()}] Running tattle.py")
        subprocess.run(["python3", "tattle.py"])
    else:
        print("rewrite.py failed.")


while True:

    config = load_config()

    scheduler = config["scheduler"]

    if not scheduler["enabled"]:
        time.sleep(10)
        continue

    start = scheduler["start_hour"]
    end = scheduler["end_hour"]

    now = datetime.now()

    if now.hour < start or now.hour >= end:
        time.sleep(60)
        continue

    # Random delay within the next 0-59 minutes
    delay = random.randint(0, 3599)

    print(f"Sleeping {delay} seconds...")

    time.sleep(delay)

    # Reload config in case the user disabled it while waiting
    config = load_config()

    if config["scheduler"]["enabled"]:
        run_job()

    # Prevent multiple runs in the same hour
    now = datetime.now()
    next_hour = (
        now.replace(minute=0, second=0, microsecond=0)
        + timedelta(hours=1)
    )

    sleep = (next_hour - now).total_seconds()

    time.sleep(sleep)
