"""Tests for Draft Grant Proposal workflow."""

from unittest.mock import patch

from src.schemas import DraftGrantInput, DraftGrantOutput
from src.services.draft_grant_proposal import run_draft_grant_proposal


@patch("src.services.draft_grant_proposal.save_artifact")
@patch("src.services.draft_grant_proposal.llm_complete_chat")
def test_draft_grant_returns_output_and_saves(mock_llm, mock_save):
    """Returns DraftGrantOutput with draft_sections and suggested_headings; saves artifact."""
    mock_llm.return_value = "NEED STATEMENT:\n\nWe serve veterans.\n\nPROGRAM DESCRIPTION:\n\nOur program..."
    inp = DraftGrantInput(
        program_name="Riding for Wellness",
        amount_requested="$10,000",
        purpose="Equipment",
        audience="veterans",
        deadline="March 2026",
    )
    out = run_draft_grant_proposal(inp)
    assert isinstance(out, DraftGrantOutput)
    assert "NEED STATEMENT" in out.draft_sections
    assert "veterans" in out.draft_sections
    assert len(out.suggested_headings) <= 10
    mock_save.assert_called_once_with("grant_draft", out.draft_sections, {"program": "Riding for Wellness"})


@patch("src.services.draft_grant_proposal.save_artifact")
@patch("src.services.draft_grant_proposal.llm_complete_chat")
def test_draft_grant_default_headings_when_none_extracted(mock_llm, mock_save):
    """When no headings match heuristic, suggested_headings is default list."""
    mock_llm.return_value = "One long paragraph with no section titles here at all."
    inp = DraftGrantInput(
        program_name="Test",
        amount_requested="$5,000",
        purpose="Scholarships",
    )
    out = run_draft_grant_proposal(inp)
    assert out.draft_sections == mock_llm.return_value
    assert out.suggested_headings == [
        "Need Statement",
        "Program Description",
        "Goals",
        "Budget Narrative",
    ]
    mock_save.assert_called_once()


@patch("src.services.draft_grant_proposal.save_artifact")
@patch("src.services.draft_grant_proposal.llm_complete_chat")
def test_draft_grant_llm_failure_returns_fallback(mock_llm, mock_save):
    """When LLM raises, returns fallback output and does not save."""
    mock_llm.side_effect = RuntimeError("API error")
    inp = DraftGrantInput(
        program_name="Test",
        amount_requested="$1,000",
        purpose="Ops",
    )
    out = run_draft_grant_proposal(inp)
    assert "could not be generated" in out.draft_sections
    assert out.suggested_headings == [
        "Need Statement",
        "Program Description",
        "Goals",
        "Budget Narrative",
    ]
    mock_save.assert_not_called()
