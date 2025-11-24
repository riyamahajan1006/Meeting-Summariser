# pages/3_Record_Live_Meeting.py
import streamlit as st
from recorder import record_meeting, list_devices
from transcriber import transcribe_audio
from analyser import analyse_meeting
import os

st.set_page_config(page_title="Record Live Meeting", layout="wide")
st.title("🔴 Record Live Meeting")

st.info("To capture everyone in the meeting you need a virtual audio cable (VB-Cable / BlackHole) and set the OS output to the cable.")

meet_link = st.text_input("Enter Google Meet link (optional):", "")
duration = st.number_input("Record duration (seconds)", min_value=5, max_value=3600, value=60)
device_name = st.text_input("Input device name substring (leave blank to use default). Use list_devices() to inspect.", value="")

if st.button("List audio devices"):
    devices = list_devices()
    st.write(devices)

if st.button("Start recording"):
    try:
        st.info("Recording... Keep the meeting audio playing. This may take a while.")
        filepath = record_meeting(meet_link.strip(), duration_seconds=duration, device_name=(device_name.strip() or None))
        st.success(f"Saved recording: {filepath}")

        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(file_path=filepath, language="en-IN")

        st.subheader("Transcript")
        st.text_area("Transcript", transcript, height=300)

        st.subheader("Analysis")
        result = analyse_meeting(transcript)
        st.write("Summary:", result["summary"])
        st.write("Keywords:", ", ".join(result["keywords"]))
        st.json(result["sentiment"])

        # download links
        st.download_button("Download Transcript", transcript, file_name="meeting_transcript.txt")
    except Exception as e:
        st.error(f"Recording/transcription failed: {e}")
