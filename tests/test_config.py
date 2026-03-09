"""Tests for config behavior (ensure_data_dir)."""

from unittest.mock import patch

from src import config


def test_ensure_data_dir_creates_directory(tmp_path):
    """ensure_data_dir() creates DATA_DIR if it does not exist."""
    target = tmp_path / "data"
    assert not target.exists()
    with patch.object(config, "DATA_DIR", target):
        config.ensure_data_dir()
    assert target.exists()
    assert target.is_dir()
