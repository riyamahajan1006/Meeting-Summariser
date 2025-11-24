# app.py
import streamlit as st

st.set_page_config(page_title="Meeting Summariser", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.write("Pages:")

st.title("🧠 Meeting Summariser")
st.markdown(
    """
    Welcome! Use the sidebar (or top links) to:
    - Transcribe uploaded audio.
    - Analyse a transcript.
    - Record a live Google Meet (requires virtual audio cable to capture all voices).
    """
)
st.info("Use the sidebar pages to open features.")
