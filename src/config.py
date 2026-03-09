from pathlib import Path
import os
import logging

ROOT_DIR = Path(__file__).resolve().parent.parent

# Data directory: use DATA_DIR env if set, else ROOT_DIR / "data"
_data_dir = os.getenv("DATA_DIR")
if _data_dir:
    DATA_DIR = Path(_data_dir)
else:
    DATA_DIR = ROOT_DIR / "data"

# SQLite path: use SQLITE_PATH env if set, else DATA_DIR / "app.db"
_sqlite_path = os.getenv("SQLITE_PATH")
if _sqlite_path:
    SQLITE_PATH = Path(_sqlite_path)
else:
    SQLITE_PATH = DATA_DIR / "app.db"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
MAX_TOKENS_SOCIAL_POST = int(os.getenv("MAX_TOKENS_SOCIAL_POST", "512"))
MAX_TOKENS_NEWSLETTER = int(os.getenv("MAX_TOKENS_NEWSLETTER", "1024"))
MAX_TOKENS_GRANT = int(os.getenv("MAX_TOKENS_GRANT", "2048"))


def ensure_data_dir() -> None:
    """Create the data directory if it does not exist. Call once at app startup."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_openai_api_key() -> str | None:
    """
    Return OpenAI API key with priority: Streamlit secrets first, then env OPENAI_API_KEY.
    Imports streamlit only inside this function so the app can run outside Streamlit (e.g. tests).
    """
    try:
        import streamlit as st
        key = st.secrets.get("OPENAI_API_KEY")
        if key:
            return key
    except ImportError:
        pass
    except Exception:
        pass  # e.g. st.secrets not available when not in Streamlit
    return os.getenv("OPENAI_API_KEY")


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application. Call once at startup (e.g. in app.py)."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
