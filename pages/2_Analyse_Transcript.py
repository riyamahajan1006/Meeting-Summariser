# pages/2_Analyse_Transcript.py

from json import dumps as json_dumps
import streamlit as st
from meeting_summariser import analyse_meeting

st.set_page_config(page_title="Analyse Transcript", layout="wide")
st.title("Analyse Transcript")

st.write("Paste your transcript below to extract key points, action items, topics, sentiment, and basic stats.")

# Input area
text = st.text_area("Paste transcript here", height=260, placeholder="Paste your transcript text…")

max_key_points = 7  # internal cap

if st.button("Analyse", type="primary", use_container_width=True):
    if not text or not text.strip():
        st.warning("Please paste a non-empty transcript.")
        st.stop()

    with st.spinner("Analysing transcript…"):
        try:
            result = analyse_meeting(text, key_points=max_key_points)
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.success("Analysis complete")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Key Points")
        key_points = result.get("key_points", []) or []
        if key_points:
            for p in key_points:
                st.markdown(f"- {p}")
        else:
            st.write("—")

        st.subheader("Topics")
        topics = result.get("topics", []) or []
        st.write(", ".join(topics) if topics else "—")

    with col2:
        st.subheader("Action Items")
        actions = result.get("action_items", []) or []
        if actions:
            for a in actions:
                st.markdown(f"- {a}")
        else:
            st.write("—")

        st.subheader("Sentiment")
        s = result.get("sentiment", {"pos": 0, "neu": 0, "neg": 0, "compound": 0}) or {}
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Positive", f"{s.get('pos', 0):.2f}")
        m2.metric("Neutral", f"{s.get('neu', 0):.2f}")
        m3.metric("Negative", f"{s.get('neg', 0):.2f}")
        m4.metric("Compound", f"{s.get('compound', 0):.2f}")

        st.subheader("Stats")
        st.write(f"Words: **{result.get('word_count', 0)}**")

    # Download .json (full analysis)
    st.download_button(
        "Download Analysis (.json)",
        data=json_dumps(result, indent=2, ensure_ascii=False),
        file_name="meeting_analysis.json",
        mime="application/json",
        use_container_width=True,
    )

    # Optional: quick link back to Transcribe page
    st.page_link("pages/1_Transcribe_Audio.py", label="Need a transcript first? Go to Transcribe Audio →")
else:
    st.info("Paste a transcript and click **Analyse**.")
