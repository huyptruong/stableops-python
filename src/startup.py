"""App bootstrap: run once at startup before the UI."""

from dotenv import load_dotenv

from src.config import configure_logging, ensure_data_dir
from src.integrations.storage import init_db


def bootstrap_app() -> None:
    """
    Run all startup steps: load env, ensure data dir, configure logging, init DB.
    Call once at app entry (e.g. app.py) before any UI.
    """
    load_dotenv()
    ensure_data_dir()
    configure_logging()
    init_db()
