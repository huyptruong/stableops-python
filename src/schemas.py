"""Pydantic models for StableOps workflow inputs and outputs."""

from enum import Enum

from pydantic import BaseModel, Field


class SocialPlatform(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    BOTH = "both"


class CreatePostInput(BaseModel):
    details: str = Field(..., description="What the post is about (e.g., event, news)")
    platform: SocialPlatform = Field(default=SocialPlatform.BOTH)


class CreatePostOutput(BaseModel):
    post_text: str = Field(..., description="Generated post content")
    platform: SocialPlatform
