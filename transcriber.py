# transcriber.py
# Whisper-free, in-memory transcription.
# Default backend: Google Web Speech via speech_recognition (fast, no local model download).
# Optional offline: Vosk (requires local model folder; see notes below).

from io import BytesIO
from typing import List, Literal, Optional
import math
import speech_recognition as sr

# pydub is used ONLY in-memory for decoding & resampling; we never write files to disk.
# Requires ffmpeg installed on your system PATH for non-WAV inputs (MP3/M4A/etc).
# If you only upload WAV, ffmpeg isn't required.
from pydub import AudioSegment

def _to_wav_mono16k(in_bytes: bytes) -> bytes:
    """
    Convert arbitrary audio bytes to WAV mono 16k in-memory.
    Never writes to disk.
    """
    audio = AudioSegment.from_file(BytesIO(in_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    out = BytesIO()
    audio.export(out, format="wav")
    return out.getvalue()


def _split_wav_bytes(wav_bytes: bytes, chunk_ms: int = 60_000) -> List[bytes]:
    """
    Split WAV bytes into ~chunk_ms pieces to keep Google API reliable on long meetings.
    """
    audio = AudioSegment.from_file(BytesIO(wav_bytes), format="wav")
    chunks: List[bytes] = []
    n_chunks = math.ceil(len(audio) / chunk_ms)
    for i in range(n_chunks):
        part = audio[i * chunk_ms: (i + 1) * chunk_ms]
        out = BytesIO()
        part.export(out, format="wav")
        chunks.append(out.getvalue())
    return chunks


def transcribe(
    file_bytes: bytes,
    language: str = "en-IN",
    backend: Literal["google", "vosk"] = "google",
    vosk_model_path: Optional[str] = None,
) -> str:
    """
    Transcribe audio entirely in-memory.
    - backend="google": uses Google Web Speech (fast, no local model download).
      Requires internet. No files written locally.
    - backend="vosk":   offline; requires 'vosk' pip pkg and a local model path.
                        (Not used unless you pass backend="vosk" and set vosk_model_path)

    Returns a single transcript string.
    """
    # Always convert to WAV mono 16k in memory
    wav_bytes = _to_wav_mono16k(file_bytes)

    if backend == "vosk":
        if vosk_model_path is None:
            raise ValueError("For backend='vosk' you must supply vosk_model_path.")
        try:
            from vosk import Model, KaldiRecognizer
            import json
        except Exception as e:
            raise RuntimeError("Please 'pip install vosk' to use the Vosk backend.") from e

        model = Model(vosk_model_path)
        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)

        # Stream in small blocks
        # Since we already have PCM WAV 16k mono, we can read frames directly.
        import wave
        wav_buf = BytesIO(wav_bytes)
        with wave.open(wav_buf, "rb") as wf:
            transcript_parts = []
            while True:
                data = wf.readframes(4000)  # ~0.25 sec at 16kHz
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    text = json.loads(res).get("text", "")
                    if text:
                        transcript_parts.append(text)
            final_res = rec.FinalResult()
            text = json.loads(final_res).get("text", "")
            if text:
                transcript_parts.append(text)
        return " ".join(transcript_parts).strip()

    # Default: Google Web Speech via speech_recognition (no local model download)
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # light denoise
    recognizer.dynamic_energy_threshold = True
    
    chunks = _split_wav_bytes(wav_bytes, chunk_ms=60_000)
    texts: List[str] = []
    for idx, ch in enumerate(chunks):
        with sr.AudioFile(BytesIO(ch)) as source:
            audio = recognizer.record(source)
        try:
            # language like 'en-IN', 'en-US', 'hi-IN' are supported
            t = recognizer.recognize_google(audio, language=language)
            if t:
                texts.append(t)
        except sr.UnknownValueError:
            # Skip inaudible chunk
            continue
        except sr.RequestError as e:
            raise RuntimeError(f"Google Speech request failed: {e}")
    return " ".join(texts).strip()