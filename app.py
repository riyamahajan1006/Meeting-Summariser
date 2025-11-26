# app.py
import streamlit as st

st.set_page_config(
    page_title="Meeting Summariser",
    layout="wide"
)

# ====================== SIDEBAR INFO ======================
with st.sidebar:
    st.title("About Project")
    st.info(
        """
        **Meeting Summariser** 🎙  
        - Records live meeting audio  
        - Transcribes speech into text  
        - Generates AI summary  
        - Extracts key points & sentiment  
        """
    )

# ====================== HOME PAGE =========================
st.title("Meeting Summariser DashBoard")

st.markdown(
    """
    Welcome!  
    Use the left navigation pages to:

    **1.  Record Meetings**  
    **2.  Transcribe Audio Files**  
    **3.  Summarise & Analyse Meetings**  
    """
)
