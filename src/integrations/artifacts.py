"""Artifact storage: re-exports from storage (SQLite). All app data is in the same database."""

from src.integrations.storage import load_artifacts, save_artifact

__all__ = ["save_artifact", "load_artifacts"]
