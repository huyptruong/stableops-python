"""Tests for Create Newsletter workflow."""

from unittest.mock import patch

from src.schemas import CreateNewsletterInput, CreateNewsletterOutput
from src.services.create_newsletter import run_create_newsletter


@patch("src.services.create_newsletter.save_artifact")
@patch("src.services.create_newsletter.llm_complete_chat")
def test_create_newsletter_returns_parsed_json(mock_llm, mock_save):
    """When LLM returns JSON, subject and body are parsed and save_artifact is called."""
    mock_llm.return_value = '{"subject": "Fall Updates", "body": "Dear friends,\\n\\nWe have news..."}'
    inp = CreateNewsletterInput(topic="Fall 2025", highlights="New horses", tone="warm")
    out = run_create_newsletter(inp)
    assert isinstance(out, CreateNewsletterOutput)
    assert out.subject_line == "Fall Updates"
    assert "Dear friends" in out.body_plain
    mock_save.assert_called_once()
    call = mock_save.call_args
    assert call[0][0] == "newsletter"
    assert "Subject: Fall Updates" in call[0][1]
    assert call[0][2]["topic"] == "Fall 2025"


@patch("src.services.create_newsletter.save_artifact")
@patch("src.services.create_newsletter.llm_complete_chat")
def test_create_newsletter_plain_text_fallback(mock_llm, mock_save):
    """When LLM returns non-JSON, subject_line is default and body_plain is raw text."""
    mock_llm.return_value = "Just some plain text body."
    inp = CreateNewsletterInput(topic="News", highlights="", tone="professional")
    out = run_create_newsletter(inp)
    assert out.subject_line == "Newsletter from StableOps"
    assert out.body_plain == "Just some plain text body."
    mock_save.assert_called_once()
    call = mock_save.call_args
    assert call[0][0] == "newsletter"
    assert call[0][2]["topic"] == "News"


@patch("src.services.create_newsletter.save_artifact")
@patch("src.services.create_newsletter.llm_complete_chat")
def test_create_newsletter_llm_failure_returns_fallback(mock_llm, mock_save):
    """When LLM raises, returns fallback output and does not save."""
    mock_llm.side_effect = RuntimeError("API error")
    inp = CreateNewsletterInput(topic="Fall", highlights="", tone="warm")
    out = run_create_newsletter(inp)
    assert out.subject_line == "Generation failed"
    assert "could not be generated" in out.body_plain
    mock_save.assert_not_called()
