# transcriber.py
import speech_recognition as sr
import tempfile
from pydub import AudioSegment
import os

def _to_wav(input_path: str) -> str:
    """
    Convert any supported audio to a WAV file and return its path.
    pydub/ffmpeg is used under the hood.
    """
    base = input_path
    out_wav = input_path + ".converted.wav"
    try:
        audio = AudioSegment.from_file(base)
        audio = audio.set_channels(1)  # mono for best recognition
        audio.export(out_wav, format="wav")
        return out_wav
    except Exception as e:
        # if conversion fails, return original path and let SR try
        return base

def transcribe_audio(file_bytes=None, file_path: str = None, language: str = "en-IN") -> str:
    """
    Accepts uploaded file bytes (Streamlit) or a local file_path.
    Returns transcript string.
    """
    if not file_bytes and not file_path:
        raise ValueError("Provide either file_bytes or file_path")

    # Create temporary file if bytes provided
    if file_bytes:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".tmp")
        tmp.write(file_bytes)
        tmp.flush()
        tmp.close()
        input_path = tmp.name
    else:
        input_path = file_path

    # Convert to WAV using pydub (better compatibility)
    wav_path = _to_wav(input_path)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError:
        return "[SpeechRecognition API error]"
    except Exception as e:
        return f"[Transcription failed: {e}]"
    finally:
        # cleanup temp files we created
        if file_bytes:
            try:
                os.remove(input_path)
            except Exception:
                pass
        if wav_path and file_bytes:
            try:
                os.remove(wav_path)
            except Exception:
                pass
