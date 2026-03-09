"""Create Newsletter workflow: generate subject and body for therapeutic riding program."""

import json
import logging
import re

from src.config import MAX_TOKENS_NEWSLETTER
from src.integrations.artifacts import save_artifact
from src.integrations.llm import llm_complete_chat
from src.prompts.newsletter import NEWSLETTER_SYSTEM, NEWSLETTER_USER
from src.schemas import CreateNewsletterInput, CreateNewsletterOutput

logger = logging.getLogger(__name__)


def run_create_newsletter(inp: CreateNewsletterInput) -> CreateNewsletterOutput:
    """Generate newsletter subject and body using LLM (or stub)."""
    user = NEWSLETTER_USER.format(
        topic=inp.topic,
        highlights=inp.highlights or "(none specified)",
        tone=inp.tone,
    )
    raw = llm_complete_chat(
        NEWSLETTER_SYSTEM,
        user,
        max_tokens=MAX_TOKENS_NEWSLETTER,
    )
    subject_line = "Newsletter from StableOps"
    body_plain = raw
    # Try to parse JSON; strip markdown code fence if present
    text = raw.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            subject_line = parsed.get("subject", subject_line) or subject_line
            body_plain = parsed.get("body", raw) or raw
    except (json.JSONDecodeError, TypeError):
        pass
    out = CreateNewsletterOutput(
        subject_line=subject_line,
        body_plain=body_plain,
        body_html="",
    )
    full = f"Subject: {out.subject_line}\n\n{out.body_plain}"
    save_artifact("newsletter", full, {"topic": inp.topic})
    return out
