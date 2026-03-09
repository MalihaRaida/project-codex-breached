"""Database connectivity and query helpers."""

import os
from contextlib import contextmanager

import pymysql


def db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "breached"),
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": False,
    }


@contextmanager
def get_connection():
    conn = pymysql.connect(**db_config())
    try:
        yield conn
    finally:
        conn.close()


def compromised_pair_exists(email_hash: str, password_hash: str) -> bool:
    sql = """
        SELECT 1
        FROM users
        WHERE email_hash = %s AND password_hash = %s
        LIMIT 1
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email_hash, password_hash))
            row = cur.fetchone()
            return row is not None
