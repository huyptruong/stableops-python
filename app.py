import streamlit as st

from src.config import configure_logging
from src.integrations.storage import init_db
from src.schemas import CreatePostInput, SocialPlatform
from src.services.create_social_post import run_create_social_post

configure_logging()
init_db()

st.set_page_config(page_title="StableOps", page_icon="🐴", layout="centered")
st.title("🐴 StableOps")
st.caption("AI-powered tools for therapeutic riding programs")

page = st.sidebar.radio(
    "Workflow",
    ["Create Social Post"],
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
