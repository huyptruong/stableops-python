from pathlib import Path
import os
import logging

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent

# Data directory: use DATA_DIR env if set, else ROOT_DIR / "data"
_data_dir = os.getenv("DATA_DIR")
if _data_dir:
    DATA_DIR = Path(_data_dir)
else:
    DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite path: use SQLITE_PATH env if set, else DATA_DIR / "app.db"
_sqlite_path = os.getenv("SQLITE_PATH")
if _sqlite_path:
    SQLITE_PATH = Path(_sqlite_path)
else:
    SQLITE_PATH = DATA_DIR / "app.db"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application. Call once at startup (e.g. in app.py)."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
