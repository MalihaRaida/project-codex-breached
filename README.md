# Breached

Breached is a Flask + MySQL web application that helps users check whether an email/password pair appears in a known breach dataset **without storing or transmitting plaintext credentials**.

## Features

- Loads breached credentials into MySQL as SHA-256 hashes
- Verifies candidate credentials through a simple web form
- Uses only hashed values in DB queries
- Supports environment-variable based configuration

## Tech

- Python 3
- Flask
- MySQL
- Cryptographic hashing (`hashlib.sha256`)

## Project layout

- `app.py` – Flask app and HTTP routes
- `db.py` – MySQL connection helper
- `hashing.py` – SHA-256 hashing helpers
- `load_breach_data.py` – Part 1 loader script for breached data
- `templates/index.html` – UI for checking credentials
- `schema.sql` – SQL schema for `users` table
- `.env.example` – Example environment variables
- `requirements.txt` – Python dependencies

## Setup

1. Create a MySQL database.
2. Apply schema:
   ```bash
   mysql -u root -p breached < schema.sql
   ```
3. Create and activate a virtual environment, then install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Configure environment variables (copy `.env.example` to `.env` and edit values).

## Part 1: Load breached data (hashed)

Input CSV format expected by loader:

```csv
email,password
alice@example.com,Password123
bob@example.com,qwerty
```

Run:

```bash
python load_breach_data.py --file breached_pairs.csv
```

The loader will:
- Normalize and hash email/password with SHA-256
- Insert pairs into `users(email_hash, password_hash)`
- Ignore duplicates safely

## Part 2: Web verification service

Start Flask server:

```bash
python app.py
```

Open `http://127.0.0.1:5000` and submit an email + password.

Results:
- **Compromised**: exact email/password hash pair exists
- **Not found**: pair does not exist in breach table

## Security notes

- Plaintext email/password are never saved in DB.
- Hashing occurs before querying/inserting.
- For stronger production security, prefer a keyed HMAC or k-anonymity approach to reduce hash enumeration risk.
