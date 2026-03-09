"""Prompts for Create Newsletter workflow."""

NEWSLETTER_SYSTEM = """You are writing a newsletter for a therapeutic riding nonprofit.
Write a warm, professional email that highlights program news, events, and impact.
Include a compelling subject line and a clear call to action. Keep paragraphs short.

You must respond with only a JSON object—no other text, no markdown, no explanation.
Use exactly this format: {"subject": " ", "body": " "}."""

NEWSLETTER_USER = """Draft a newsletter with:

Topic: {topic}
Highlights to include: {highlights}
Tone: {tone}

Respond with only a JSON object in this exact format (no other text):
{{"subject": " ", "body": " "}}"""
