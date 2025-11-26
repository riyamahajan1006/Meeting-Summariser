# pages/2_Analyse_Transcript.py
import streamlit as st
import json
from analyser import analyse, save_output_to_json

st.title("Analyse Meeting Transcript")

uploaded = st.file_uploader("Upload Transcript (.txt)", type=["txt"])

if uploaded:
    text = uploaded.read().decode("utf-8")
    st.subheader("Transcript Preview")
    st.write(text[:1500] + ("..." if len(text) > 1500 else ""))

    if st.button("Analyse"):
        with st.spinner("Analysing... "):
            result = analyse(text)
            save_output_to_json(text)

        st.success("Analysis Completed!")

        st.subheader("1. Summary")
        st.write(result["summary"])

        st.subheader("2.  Keywords")
        st.write(result["keywords"])

        st.subheader("3.  Sentiment")
        st.write(result["sentiment"])

        st.download_button(
            label="Download JSON Output",
            data=json.dumps(result, indent=4),
            file_name="analysis_output.json",
            mime="application/json"
        )
