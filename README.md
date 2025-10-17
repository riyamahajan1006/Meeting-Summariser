# 📝 Meeting Summariser

**Meeting Summariser** is a Streamlit-based web application that converts your meeting audio into a clean transcript, extracts key discussion points, generates concise summaries, and performs sentiment analysis — all processed **entirely in memory** for speed and privacy.

---

## 🚀 Features

- 🎙️ **Audio → Transcript:**  
  Upload a recorded meeting audio file (`.mp3`, `.wav`, etc.) and get instant transcription using **Google Speech Recognition** (online) or **Vosk** (offline).

- 🧾 **Transcript → Analysis:**  
  Paste or load any transcript text to get:
  - Key discussion points  
  - Action items (automatically inferred)  
  - Sentiment summary (positive / neutral / negative)

- ⚡ **Lightweight & Fast:**  
  No Whisper or heavy GPU models — ideal for regular laptops.  
  All audio is processed in memory (not saved on disk).

- 🌐 **User-friendly Web Interface:**  
  Built using Streamlit with a clean layout:
  - **Home page:** Introduction and project overview  
  - **Page 1:** Upload and transcribe audio  
  - **Page 2:** Analyse text for summary and sentiment  

---
