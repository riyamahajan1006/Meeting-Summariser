# app.py
# Run: streamlit run app.py

import streamlit as st

st.set_page_config(page_title="Meeting Summariser", layout="wide")

st.title("Meeting Summariser")

# ---------- Sidebar: About this project ----------
with st.sidebar:
    st.header("About this project")
    st.markdown(
        """
**Meeting Summariser** helps you:
- Convert meeting audio into a transcript (fast, in-memory).
- Extract **key points** and **action items**.
- Detect **topics**.
- Perform **sentiment analysis**.
- Download results as **.txt** (transcript) and **.json** (analysis).

**Two ways to use it**
1. **Transcribe Audio:** Upload audio → get transcript (+ copy).
2. **Analyse Transcript:** Paste a transcript → get analysis.
        """
    )

st.write("Choose what you want to do:")

# ---------- Big navigation cards ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Transcribe Audio")
    st.write("Upload an MP3/WAV/etc. and get a clean transcript you can copy or download.")
    st.page_link("pages/1_Transcribe_Audio.py", label="Go to Transcribe Audio →")

with col2:
    st.subheader("Analyse Transcript")
    st.write("Paste an existing transcript and get key points, action items, topics, and sentiment.")
    st.page_link("pages/2_Analyse_Transcript.py", label="Go to Analyse Transcript →")

st.info("Tip: You can always switch pages from the left sidebar menu at the top of the app.")
