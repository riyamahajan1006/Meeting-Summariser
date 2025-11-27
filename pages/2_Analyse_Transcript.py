import streamlit as st
import json
from analyser import analyse, save_output_to_json

st.title("Analyse Meeting Transcript")

# Dropdown to choose input type
choice = st.selectbox(
    "Choose how you want to provide the transcript",
    ["Paste Transcript", "Upload Text File"]
)

text = ""

# Show only one input based on selection
if choice == "Paste Transcript":
    text_area = st.text_area("Paste your meeting transcript here")
    if text_area.strip():
        text = text_area.strip()

elif choice == "Upload Text File":
    uploaded = st.file_uploader("Upload Transcript (.txt)", type=["txt"])
    if uploaded:
        text = uploaded.read().decode("utf-8")

# Manual input for summary word count
summary_len = st.number_input(
    "Enter number of words for summary",
    min_value=50,
    max_value=2000,
    value=120,
    step=10,
)

# Show transcript preview if available
if text:
    st.subheader("Transcript Preview")
    st.write(text[:1500] + ("..." if len(text) > 1500 else ""))

# Analyse button
if st.button("Analyse Transcript"):
    if not text:
        st.warning("Please provide a transcript first.")
    else:
        with st.spinner("Analysing your transcript..."):
            result = analyse(text, summary_len)
            save_output_to_json(text)

        st.success("Analysis Completed")

        st.subheader("1. Summary")
        st.write(result["summary"])

        st.subheader("2. Keywords")
        st.write(result["keywords"])

        st.subheader("3️. Sentiment Analysis")
        st.write(result["sentiment"])

        st.subheader("4️. Transcript Statistics")
        st.write(result["stats"])

        st.download_button(
            label="Download Analysis JSON",
            data=json.dumps(result, indent=4),
            file_name="analysis_output.json",
            mime="application/json"
        )
