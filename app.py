from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
)

import json
import subprocess
import sys
import os
from functools import wraps


# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


# ----------------------------------------------------
# Config Helpers
# ----------------------------------------------------

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    temp_file = CONFIG_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(config, f, indent=4)

    os.replace(temp_file, CONFIG_FILE)


# ----------------------------------------------------
# Flask App
# ----------------------------------------------------

app = Flask(__name__)

# Change this to a long random string.
# This is NOT your login password.
app.secret_key = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"


# ----------------------------------------------------
# Login Decorator
# ----------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


# ----------------------------------------------------
# Login
# ----------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    config = load_config()
    password = config["password"]

    if session.get("logged_in"):
        return redirect(url_for("index"))

    error = None

    if request.method == "POST":

        submitted_password = request.form.get("password", "")

        if submitted_password == password:
            session["logged_in"] = True
            return redirect(url_for("index"))

        error = "Incorrect password"

    return render_template("login.html", error=error)


# ----------------------------------------------------
# Logout
# ----------------------------------------------------

@app.route("/logout")
@login_required
def logout():

    session.clear()

    return redirect(url_for("login"))


# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

@app.route("/")
@login_required
def index():

    config = load_config()
    scheduler = config.get("scheduler", {})

    return render_template(
        "index.html",
        scheduler=scheduler,
    )


# ----------------------------------------------------
# Manual Rewrite
# ----------------------------------------------------

@app.route("/rewrite")
@login_required
def rewrite():

    subprocess.run(
        [sys.executable, "rewrite.py"],
        cwd=BASE_DIR,
    )

    return redirect(url_for("index"))


# ----------------------------------------------------
# Manual Tattle
# ----------------------------------------------------

@app.route("/tattle")
@login_required
def tattle():

    subprocess.run(
        [sys.executable, "tattle.py"],
        cwd=BASE_DIR,
    )

    return redirect(url_for("index"))


# ----------------------------------------------------
# Manual Run Both
# ----------------------------------------------------

@app.route("/run")
@login_required
def run():

    result = subprocess.run(
        [sys.executable, "rewrite.py"],
        cwd=BASE_DIR,
    )

    if result.returncode == 0:
        subprocess.run(
            [sys.executable, "tattle.py"],
            cwd=BASE_DIR,
        )

    return redirect(url_for("index"))


# ----------------------------------------------------
# Scheduler Start
# ----------------------------------------------------

@app.route("/scheduler/start")
@login_required
def scheduler_start():

    config = load_config()

    config["scheduler"]["enabled"] = True
    config["scheduler"]["status"] = "Running"

    save_config(config)

    return redirect(url_for("index"))


# ----------------------------------------------------
# Scheduler Stop
# ----------------------------------------------------

@app.route("/scheduler/stop")
@login_required
def scheduler_stop():

    config = load_config()

    config["scheduler"]["enabled"] = False
    config["scheduler"]["status"] = "Stopped"
    config["scheduler"]["next_run"] = None

    save_config(config)

    return redirect(url_for("index"))


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
