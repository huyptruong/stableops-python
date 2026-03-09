"""Create Social Post workflow: generate social post content for therapeutic riding program."""

import logging

from src.config import MAX_TOKENS_SOCIAL_POST
from src.integrations.artifacts import save_artifact
from src.integrations.llm import llm_complete_chat
from src.prompts.social_post import SOCIAL_POST_SYSTEM, SOCIAL_POST_USER
from src.schemas import CreatePostInput, CreatePostOutput, SocialPlatform

logger = logging.getLogger(__name__)


def run_create_social_post(inp: CreatePostInput, *, use_llm: bool = True) -> CreatePostOutput:
    """
    Create social post content. If use_llm and an API key is set, uses LLM;
    otherwise uses template fallback (Instagram/Facebook blocks).
    """
    if use_llm:
        try:
            user = SOCIAL_POST_USER.format(
                details=inp.details,
                platform=inp.platform.value,
            )
            post_text = llm_complete_chat(
                SOCIAL_POST_SYSTEM,
                user,
                max_tokens=MAX_TOKENS_SOCIAL_POST,
            )
            out = CreatePostOutput(post_text=post_text.strip(), platform=inp.platform)
            save_artifact("social_post", out.post_text, {"platform": out.platform.value})
            return out
        except Exception as e:
            logger.exception("LLM call failed for social post, using template fallback: %s", e)

    # Fallback when LLM is not available or use_llm is False
    post = ""
    if inp.platform in (SocialPlatform.INSTAGRAM, SocialPlatform.BOTH):
        post += (
            f"🐴 {inp.details}\n\n"
            "Join us and be part of something special! ❤️\n\n"
            "#therapeuticriding #horses #community #nonprofit\n\n"
        )
    if inp.platform in (SocialPlatform.FACEBOOK, SocialPlatform.BOTH):
        post += (
            "We're excited to share some news from our farm!\n\n"
            f"{inp.details}\n\n"
            "We'd love to see you there. Tag a friend who would enjoy this! 🐎"
        )
    out = CreatePostOutput(post_text=post.strip(), platform=inp.platform)
    save_artifact("social_post", out.post_text, {"platform": out.platform.value})
    return out
