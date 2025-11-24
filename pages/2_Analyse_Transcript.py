# pages/2_Analyse_Transcript.py
import streamlit as st
from analyser import analyse_meeting

st.title("📊 Analyse Transcript")

text = st.text_area("Paste transcript here:", height=300)

if st.button("Analyse"):
    if not text.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("Analysing..."):
            res = analyse_meeting(text)
        st.subheader("Summary")
        st.write(res["summary"])
        st.subheader("Keywords")
        st.write(", ".join(map(str, res["keywords"])))
        st.subheader("Sentiment")
        st.json(res["sentiment"])
        st.write("Words:", res.get("word_count", 0))
