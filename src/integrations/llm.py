import logging

from openai import OpenAI

from src.config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    OPENAI_MODEL,
    get_openai_api_key,
)

logger = logging.getLogger(__name__)


def llm_complete_chat(
    system_prompt: str,
    user_prompt: str,
    *,
    max_tokens: int = 512,
) -> str:
    """Chat-style completion with system + user message. Uses OpenAI first, then Anthropic, else stub."""
    if get_openai_api_key():
        try:
            return _openai_chat(system_prompt, user_prompt, max_tokens=max_tokens)
        except Exception as e:
            logger.exception("OpenAI chat failed: %s", e)
            raise RuntimeError(f"LLM request failed: {e}") from e
    if ANTHROPIC_API_KEY:
        try:
            return _anthropic_chat(system_prompt, user_prompt, max_tokens=max_tokens)
        except Exception as e:
            logger.exception("Anthropic chat failed: %s", e)
            raise RuntimeError(f"LLM request failed: {e}") from e
    logger.info("No LLM API key set; returning stub response")
    return _stub_chat(user_prompt)


def _openai_chat(system_prompt: str, user_prompt: str, *, max_tokens: int) -> str:
    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError("OpenAI API key not configured")
    client = OpenAI(api_key=api_key)
    r = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
    )
    return (r.choices[0].message.content or "").strip()


def _anthropic_chat(system_prompt: str, user_prompt: str, *, max_tokens: int) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    r = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return (r.content[0].text if r.content else "").strip()


def _stub_chat(user_prompt: str) -> str:
    return (
        "[Demo mode — no API key set]\n\n"
        "Set OPENAI_API_KEY or ANTHROPIC_API_KEY in your environment (or .env) to get real AI output.\n\n"
        "User request was:\n" + user_prompt[:500]
    )
