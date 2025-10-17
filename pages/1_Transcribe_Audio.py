# pages/1_Transcribe_Audio.py

from io import BytesIO
from json import dumps as json_dumps
import json

import streamlit as st

from transcriber import transcribe  # uses your existing function

st.set_page_config(page_title="Transcribe Audio", page_icon="🎙️", layout="wide")
st.title("🎙️ Transcribe Audio")

st.write("Upload an audio file to generate a transcript. Nothing is written to disk — all in memory.")

backend = "google"   # fixed as requested
language = "en-IN"
vosk_model_path = None

audio_file = st.file_uploader(
    "Upload audio (MP3/WAV/M4A/AAC/OGG/FLAC)",
    type=["mp3", "wav", "m4a", "aac", "ogg", "flac"]
)

if audio_file is not None:
    file_bytes = audio_file.read()
    mime = audio_file.type or "audio/mpeg"
    st.audio(BytesIO(file_bytes), format=mime)

    if st.button("Transcribe", type="primary", use_container_width=True):
        with st.spinner("Transcribing…"):
            try:
                text = transcribe(
                    file_bytes=file_bytes,
                    language=language,
                    backend=backend,
                    vosk_model_path=vosk_model_path,
                )
            except Exception as e:
                st.error(f"Transcription failed: {e}")
                st.stop()

        if not text or not text.strip():
            st.warning("No speech detected or transcription is empty.")
            st.stop()

        st.success("Transcription complete ✅")

        st.subheader("📝 Transcript")

        # Show transcript in a read-only, scrollable box.
        st.text_area("Transcript", value=text, height=280, label_visibility="collapsed")

        # --- Copy to clipboard button (client-side) ---
        escaped = json.dumps(text)  # safe for JS
        st.markdown(
            f"""
            <button id="copyBtn" style="margin-top:0.5rem;padding:0.4rem 0.8rem;border-radius:0.5rem;border:1px solid #ddd;">
              Copy transcript
            </button>
            <script>
            const btn = document.getElementById('copyBtn');
            if (btn) {{
              btn.addEventListener('click', async () => {{
                try {{
                  await navigator.clipboard.writeText({escaped});
                  const old = btn.innerText;
                  btn.innerText = "Copied!";
                  setTimeout(() => btn.innerText = old, 1200);
                }} catch (err) {{
                  alert("Copy failed: " + err);
                }}
              }});
            }}
            </script>
            """,
            unsafe_allow_html=True,
        )

        # Download .txt
        st.download_button(
            "⬇️ Download Transcript (.txt)",
            data=text,
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )

        # Quick link to analysis page with instructions
        st.info("Next step: paste this transcript into **Analyse Transcript** to get key points, action items, topics, and sentiment.")
        st.page_link("pages/2_Analyse_Transcript.py", label="Go to Analyse Transcript →", icon="➡️")
else:
    st.info("Please upload an audio file to begin.")
