import sqlite3
import logging
from datetime import datetime, timezone

from src.config import SQLITE_PATH

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(SQLITE_PATH)


def init_db() -> None:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    except Exception as e:
        logger.exception("Database initialization failed")
        raise RuntimeError(f"Database init failed: {e}") from e


def save_generation(prompt: str, response: str) -> None:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO generations (prompt, response, created_at)
            VALUES (?, ?, ?)
            """,
            (prompt, response, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()
        logger.debug("Generation saved")
    except Exception as e:
        logger.exception("Failed to save generation")
        raise RuntimeError(f"Failed to save generation: {e}") from e
