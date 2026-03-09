import logging

from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


def llm_complete(prompt: str) -> str:
    """Return a text completion from OpenAI, or a stub if no API key exists."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set; returning stub response")
        return f"[STUB RESPONSE] No OPENAI_API_KEY found.\n\nPrompt was:\n{prompt}"

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )
        logger.info("LLM completion succeeded")
        return response.output_text
    except Exception as e:
        logger.exception("LLM API request failed")
        raise RuntimeError(f"LLM request failed: {e}") from e
