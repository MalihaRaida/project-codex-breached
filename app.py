"""Flask web app for breached credential verification."""

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from db import compromised_pair_exists
from hashing import hash_email, hash_password

load_dotenv()

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/check")
def check():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if not email or not password:
        return render_template(
            "index.html",
            status="Please provide both email and password.",
            compromised=None,
        )

    email_hash = hash_email(email)
    password_hash = hash_password(password)
    compromised = compromised_pair_exists(email_hash, password_hash)

    status = (
        "This email/password combination appears in the breach dataset."
        if compromised
        else "No exact match found in the breach dataset."
    )

    return render_template("index.html", status=status, compromised=compromised)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
