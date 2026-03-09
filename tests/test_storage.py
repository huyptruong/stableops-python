"""Tests for artifact storage (save_artifact, load_artifacts)."""

from unittest.mock import patch

from src.integrations.storage import init_db, load_artifacts, save_artifact


def test_save_artifact_returns_id_and_persists(tmp_path):
    """Saving an artifact returns an id and the artifact can be loaded back."""
    with patch("src.integrations.storage.SQLITE_PATH", tmp_path / "test.db"):
        init_db()
        id1 = save_artifact("social_post", "Hello world", {"platform": "instagram"})
        assert len(id1) == 8
        loaded = load_artifacts()
        assert len(loaded) == 1
        assert loaded[0]["id"] == id1
        assert loaded[0]["kind"] == "social_post"
        assert loaded[0]["content"] == "Hello world"
        assert loaded[0]["meta"] == {"platform": "instagram"}
        assert "created_at" in loaded[0]


def test_load_artifacts_empty_returns_empty_list(tmp_path):
    """Loading with no artifacts returns an empty list."""
    with patch("src.integrations.storage.SQLITE_PATH", tmp_path / "test.db"):
        init_db()
        result = load_artifacts()
        assert result == []


def test_load_artifacts_filter_by_kind(tmp_path):
    """load_artifacts(kind=...) returns only artifacts of that kind, newest first."""
    with patch("src.integrations.storage.SQLITE_PATH", tmp_path / "test.db"):
        init_db()
        save_artifact("social_post", "Post A")
        save_artifact("newsletter", "News B")
        save_artifact("social_post", "Post C")
        all_ = load_artifacts(limit=10)
        assert len(all_) == 3
        social = load_artifacts(kind="social_post", limit=10)
        assert len(social) == 2
        assert {r["content"] for r in social} == {"Post A", "Post C"}
        assert social[0]["content"] == "Post C"  # newest first
        newsletter = load_artifacts(kind="newsletter", limit=10)
        assert len(newsletter) == 1
        assert newsletter[0]["content"] == "News B"
