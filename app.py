import streamlit as st

from src.config import configure_logging
from src.integrations.storage import init_db
from src.services.generate_text import generate_text

configure_logging()
init_db()

st.set_page_config(page_title="Python AI Starter Template", page_icon="🤖")

st.title("Python AI Starter Template")
st.write("A minimal starter app for AI-powered Python projects.")

prompt = st.text_area("Enter your prompt", height=200)

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating response..."):
            response = generate_text(prompt)

        st.subheader("Response")
        st.write(response)
