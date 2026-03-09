import json
import sqlite3
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

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
            CREATE TABLE IF NOT EXISTS artifacts (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                content TEXT NOT NULL,
                meta TEXT NOT NULL,
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


def save_artifact(kind: str, content: str, meta: dict[str, Any] | None = None) -> str:
    """Append an artifact (e.g. 'social_post', 'newsletter', 'grant_draft') to the database. Returns id."""
    id_ = str(uuid.uuid4())[:8]
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO artifacts (id, kind, content, meta, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_, kind, content, meta_json, created_at),
        )
        conn.commit()
        conn.close()
        logger.debug("Artifact saved: kind=%s id=%s", kind, id_)
        return id_
    except Exception as e:
        logger.exception("Failed to save artifact")
        raise RuntimeError(f"Failed to save artifact: {e}") from e


def load_artifacts(kind: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    """Load recent artifacts from the database, optionally filtered by kind. Newest first."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        if kind:
            cur.execute(
                """
                SELECT id, kind, content, meta, created_at FROM artifacts
                WHERE kind = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (kind, limit),
            )
        else:
            cur.execute(
                """
                SELECT id, kind, content, meta, created_at FROM artifacts
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )
        rows = cur.fetchall()
        conn.close()
        result = []
        for row in rows:
            id_, k, content, meta_json, created_at = row
            try:
                meta = json.loads(meta_json) if meta_json else {}
            except json.JSONDecodeError:
                meta = {}
            result.append({
                "id": id_,
                "kind": k,
                "content": content,
                "meta": meta,
                "created_at": created_at,
            })
        return result
    except Exception as e:
        logger.exception("Failed to load artifacts")
        raise RuntimeError(f"Failed to load artifacts: {e}") from e
