"""Tests for Create Social Post workflow."""

from unittest.mock import patch

from src.schemas import CreatePostInput, CreatePostOutput, SocialPlatform
from src.services.create_social_post import run_create_social_post


@patch("src.services.create_social_post.save_artifact")
def test_create_social_post_fallback_instagram(mock_save):
    """With use_llm=False, Instagram-only returns template with details and hashtags."""
    inp = CreatePostInput(details="Fall festival Nov 5", platform=SocialPlatform.INSTAGRAM)
    out = run_create_social_post(inp, use_llm=False)
    assert isinstance(out, CreatePostOutput)
    assert out.platform == SocialPlatform.INSTAGRAM
    assert "Fall festival Nov 5" in out.post_text
    assert "#therapeuticriding" in out.post_text
    assert "Join us and be part of something special" in out.post_text
    mock_save.assert_called_once_with("social_post", out.post_text, {"platform": "instagram"})


@patch("src.services.create_social_post.save_artifact")
def test_create_social_post_fallback_facebook(mock_save):
    """With use_llm=False, Facebook-only returns template with details."""
    inp = CreatePostInput(details="Open house Saturday", platform=SocialPlatform.FACEBOOK)
    out = run_create_social_post(inp, use_llm=False)
    assert out.platform == SocialPlatform.FACEBOOK
    assert "Open house Saturday" in out.post_text
    assert "We're excited to share some news from our farm" in out.post_text
    mock_save.assert_called_once_with("social_post", out.post_text, {"platform": "facebook"})


@patch("src.services.create_social_post.save_artifact")
def test_create_social_post_fallback_both(mock_save):
    """With use_llm=False, BOTH includes Instagram and Facebook blocks."""
    inp = CreatePostInput(details="Holiday ride", platform=SocialPlatform.BOTH)
    out = run_create_social_post(inp, use_llm=False)
    assert out.platform == SocialPlatform.BOTH
    assert "Holiday ride" in out.post_text
    assert "#therapeuticriding" in out.post_text
    assert "We're excited to share some news from our farm" in out.post_text
    mock_save.assert_called_once_with("social_post", out.post_text, {"platform": "both"})


@patch("src.services.create_social_post.save_artifact")
@patch("src.services.create_social_post.llm_complete_chat")
def test_create_social_post_with_llm_returns_llm_response(mock_llm, mock_save):
    """With use_llm=True, returns LLM response and passes system/user prompts."""
    mock_llm.return_value = "Check out our fall event! 🐴"
    inp = CreatePostInput(details="Fall event", platform=SocialPlatform.INSTAGRAM)
    out = run_create_social_post(inp, use_llm=True)
    assert out.post_text == "Check out our fall event! 🐴"
    assert out.platform == SocialPlatform.INSTAGRAM
    mock_llm.assert_called_once()
    call_args = mock_llm.call_args
    assert "therapeutic riding" in call_args[0][0].lower()  # system prompt
    assert "Fall event" in call_args[0][1]  # user prompt has details
    assert "instagram" in call_args[0][1].lower()
    mock_save.assert_called_once_with("social_post", out.post_text, {"platform": "instagram"})


@patch("src.services.create_social_post.save_artifact")
@patch("src.services.create_social_post.llm_complete_chat")
def test_create_social_post_llm_failure_falls_back_to_template(mock_llm, mock_save):
    """When use_llm=True but LLM raises, falls back to template."""
    mock_llm.side_effect = RuntimeError("API error")
    inp = CreatePostInput(details="Rain or shine", platform=SocialPlatform.BOTH)
    out = run_create_social_post(inp, use_llm=True)
    assert "Rain or shine" in out.post_text
    assert out.platform == SocialPlatform.BOTH
    assert "#therapeuticriding" in out.post_text
    mock_save.assert_called_once_with("social_post", out.post_text, {"platform": "both"})
