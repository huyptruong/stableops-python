import logging

from src.integrations.llm import llm_complete
from src.integrations.storage import save_generation

logger = logging.getLogger(__name__)


def generate_text(prompt: str) -> str:
    """Generate text from a prompt and save the result."""
    logger.info("Generating text for prompt (length=%d)", len(prompt))
    response = llm_complete(prompt)
    save_generation(prompt, response)
    return response
