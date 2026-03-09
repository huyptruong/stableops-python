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


# --- Create Newsletter ---
class CreateNewsletterInput(BaseModel):
    topic: str = Field(..., description="Newsletter topic or theme")
    highlights: str = Field(default="", description="Key points or events to include")
    tone: str = Field(default="warm", description="Tone: warm, professional, casual")


class CreateNewsletterOutput(BaseModel):
    subject_line: str = Field(..., description="Email subject line")
    body_plain: str = Field(default="", description="Plain text version")
    body_html: str = Field(default="", description="Reserved for future HTML; currently unused")


# --- Draft Grant Proposal ---
class DraftGrantInput(BaseModel):
    program_name: str = Field(..., description="Name of the program seeking funding")
    amount_requested: str = Field(..., description="Amount and currency, e.g. $10,000")
    purpose: str = Field(..., description="What the grant will fund")
    audience: str = Field(default="", description="Target population or beneficiaries")
    deadline: str = Field(default="", description="Application or program deadline if known")


class DraftGrantOutput(BaseModel):
    draft_sections: str = Field(..., description="Draft grant narrative or sections")
    suggested_headings: list[str] = Field(default_factory=list)
