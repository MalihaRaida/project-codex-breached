"""Hashing helpers for breached credential checks."""

import hashlib


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def hash_email(email: str) -> str:
    return hash_sha256(normalize_email(email))


def hash_password(password: str) -> str:
    # Keep password bytes exactly as entered except trimming accidental outer spaces
    return hash_sha256(password.strip())
