"""Draft Grant Proposal workflow: generate grant narrative sections."""

import logging

from src.config import MAX_TOKENS_GRANT
from src.integrations.artifacts import save_artifact
from src.integrations.llm import llm_complete_chat
from src.prompts.grant import GRANT_SYSTEM, GRANT_USER
from src.schemas import DraftGrantInput, DraftGrantOutput

logger = logging.getLogger(__name__)


def run_draft_grant_proposal(inp: DraftGrantInput) -> DraftGrantOutput:
    """Draft grant proposal sections using LLM (or stub)."""
    user = GRANT_USER.format(
        program_name=inp.program_name,
        amount_requested=inp.amount_requested,
        purpose=inp.purpose,
        audience=inp.audience or "(not specified)",
        deadline=inp.deadline or "(not specified)",
    )
    draft_sections = llm_complete_chat(
        GRANT_SYSTEM,
        user,
        max_tokens=MAX_TOKENS_GRANT,
    )
    # Simple heading extraction: lines that look like section titles
    suggested_headings = []
    for line in draft_sections.split("\n"):
        s = line.strip().rstrip(":")
        if s and len(s) < 80 and (
            line.strip().endswith(":") or (len(s) > 2 and s.isupper() and len(s) < 50)
        ):
            suggested_headings.append(s)
    suggested_headings = suggested_headings[:10]
    out = DraftGrantOutput(
        draft_sections=draft_sections,
        suggested_headings=suggested_headings
        or ["Need Statement", "Program Description", "Goals", "Budget Narrative"],
    )
    save_artifact("grant_draft", out.draft_sections, {"program": inp.program_name})
    return out
