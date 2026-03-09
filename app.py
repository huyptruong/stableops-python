from src.startup import bootstrap_app

bootstrap_app()

import streamlit as st

from src.schemas import (
    CreatePostInput,
    CreateNewsletterInput,
    DraftGrantInput,
    SocialPlatform,
)
from src.services.create_social_post import run_create_social_post
from src.services.create_newsletter import run_create_newsletter
from src.services.draft_grant_proposal import run_draft_grant_proposal

st.set_page_config(page_title="StableOps", page_icon="🐴", layout="centered")
st.title("🐴 StableOps")
st.caption("AI-powered tools for therapeutic riding programs")

page = st.sidebar.radio(
    "Workflow",
    ["Create Social Post", "Create Newsletter", "Draft Grant Proposal"],
    index=0,
)

if page == "Create Social Post":
    st.header("Create Social Post")
    details = st.text_area(
        "What's this post about?",
        placeholder="E.g., Fall festival on Nov 5th, tickets $20...",
        height=120,
    )
    platform = st.radio(
        "Platform",
        [SocialPlatform.INSTAGRAM, SocialPlatform.FACEBOOK, SocialPlatform.BOTH],
        format_func=lambda x: x.value.capitalize(),
        horizontal=True,
    )
    use_llm = st.checkbox("Use AI (when API key is set)", value=True)
    if st.button("Generate Post ✨"):
        if not details.strip():
            st.warning("Please enter what the post is about.")
        else:
            with st.spinner("Generating..."):
                out = run_create_social_post(
                    CreatePostInput(details=details.strip(), platform=platform),
                    use_llm=use_llm,
                )
            st.subheader("Generated Post")
            st.text_area("Post content", value=out.post_text, height=220, key="post_result", disabled=True)
            st.download_button(
                "Download as .txt",
                data=out.post_text,
                file_name="stableops_post.txt",
                mime="text/plain",
                key="dl_post",
            )

elif page == "Create Newsletter":
    st.header("Create Newsletter")
    topic = st.text_input("Topic or theme", placeholder="E.g., Fall 2025 program updates")
    highlights = st.text_area(
        "Key points or events to include",
        placeholder="Bullet points or short paragraphs",
        height=100,
    )
    tone = st.selectbox("Tone", ["warm", "professional", "casual"], index=0)
    if st.button("Generate Newsletter ✨"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating..."):
                out = run_create_newsletter(
                    CreateNewsletterInput(
                        topic=topic.strip(),
                        highlights=highlights.strip(),
                        tone=tone,
                    ),
                )
            st.subheader("Subject line")
            st.text_input("Subject", value=out.subject_line, key="news_subj", disabled=True)
            st.subheader("Body (plain text)")
            st.text_area("Body", value=out.body_plain, height=280, key="news_body", disabled=True)
            full = f"Subject: {out.subject_line}\n\n{out.body_plain}"
            st.download_button(
                "Download as .txt",
                data=full,
                file_name="stableops_newsletter.txt",
                mime="text/plain",
                key="dl_news",
            )

elif page == "Draft Grant Proposal":
    st.header("Draft Grant Proposal")
    program_name = st.text_input("Program name", placeholder="E.g., Riding for Wellness")
    amount_requested = st.text_input("Amount requested", placeholder="E.g., $10,000")
    purpose = st.text_area(
        "What will the grant fund?",
        placeholder="Equipment, scholarships, operations...",
        height=80,
    )
    audience = st.text_input(
        "Target audience / beneficiaries",
        placeholder="E.g., veterans, children with disabilities",
    )
    deadline = st.text_input("Deadline (optional)", placeholder="E.g., March 15, 2026")
    if st.button("Generate Draft ✨"):
        if not program_name.strip() or not amount_requested.strip() or not purpose.strip():
            st.warning("Please fill in program name, amount, and purpose.")
        else:
            with st.spinner("Generating..."):
                out = run_draft_grant_proposal(
                    DraftGrantInput(
                        program_name=program_name.strip(),
                        amount_requested=amount_requested.strip(),
                        purpose=purpose.strip(),
                        audience=audience.strip(),
                        deadline=deadline.strip(),
                    ),
                )
            st.subheader("Draft sections")
            st.text_area(
                "Content",
                value=out.draft_sections,
                height=360,
                key="grant_result",
                disabled=True,
            )
            if out.suggested_headings:
                st.caption("Suggested headings: " + ", ".join(out.suggested_headings))
            st.download_button(
                "Download as .md",
                data=out.draft_sections,
                file_name="stableops_grant_draft.md",
                mime="text/markdown",
                key="dl_grant",
            )
