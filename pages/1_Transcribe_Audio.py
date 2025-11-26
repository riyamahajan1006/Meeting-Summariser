# pages/1_Transcribe_Audio.py
import streamlit as st
from transcriber import transcribe_audio

st.title("Transcribe Audio File")

audio_file = st.file_uploader("Upload an audio file (wav, mp3, m4a, flac...)", type=["wav","mp3","m4a","flac","ogg","aac"])
language = st.text_input("Language (eg. en-IN, en-US)", value="en-IN")

if audio_file:
    st.audio(audio_file)
    with st.spinner("Transcribing..."):
        transcript = transcribe_audio(file_bytes=audio_file.read(), language=language)
    st.success("Transcription finished")
    st.text_area("Transcript", transcript, height=300)
    st.download_button("Download transcript", transcript, file_name="transcript.txt")
