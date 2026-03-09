"""Load breached email/password pairs into MySQL as hashes."""

import argparse
import csv

from dotenv import load_dotenv

from db import get_connection
from hashing import hash_email, hash_password


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load breached data as SHA-256 hashes")
    parser.add_argument("--file", required=True, help="Path to CSV file containing email,password columns")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    insert_sql = """
        INSERT IGNORE INTO users (email_hash, password_hash)
        VALUES (%s, %s)
    """

    inserted = 0
    processed = 0

    with open(args.file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required_columns = {"email", "password"}
        if not required_columns.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV must contain headers: email,password")

        with get_connection() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    email = row.get("email", "")
                    password = row.get("password", "")
                    if not email or not password:
                        continue

                    processed += 1
                    email_hash = hash_email(email)
                    password_hash = hash_password(password)
                    inserted += cur.execute(insert_sql, (email_hash, password_hash))

            conn.commit()

    print(f"Processed: {processed}")
    print(f"Inserted (new): {inserted}")


if __name__ == "__main__":
    main()
