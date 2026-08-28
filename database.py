import sqlite3
from pathlib import Path

DATABASE = Path("data/codes.db")


def init_database():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS codes (
            code TEXT PRIMARY KEY,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def is_new_code(code):
    connection = sqlite3.connect(DATABASE)

    result = connection.execute(
        "SELECT 1 FROM codes WHERE code = ?",
        (code,)
    ).fetchone()

    connection.close()

    return result is None


def save_code(code):
    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "INSERT OR IGNORE INTO codes (code) VALUES (?)",
        (code,)
    )

    connection.commit()
    connection.close()
