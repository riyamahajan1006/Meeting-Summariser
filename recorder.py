# recorder.py

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
import os
import webbrowser

def list_devices():
    """Return all audio devices for debugging."""
    return sd.query_devices()

def record_meeting(meet_link: str = None,
                   duration_seconds: int = 60,
                   filename: str = "meeting_recording.wav",
                   device_name: str = None,
                   samplerate: int = 44100):
    # Open meeting link first (if provided)
    if meet_link:
        webbrowser.open(meet_link)
        time.sleep(4)  # wait to join

    # Choose device if specified
    if device_name:
        devices = sd.query_devices()
        idx = None
        for i, d in enumerate(devices):
            if device_name.lower() in d["name"].lower():
                idx = i
                break
        if idx is None:
            raise RuntimeError(
                f"Device containing '{device_name}' not found. "
                f"Use list_devices() to view options."
            )
        sd.default.device = idx

    # Recording settings
    sd.default.samplerate = samplerate
    sd.default.channels = 1  # Mono is enough and avoids errors

    # Start Recording
    frames = sd.rec(int(duration_seconds * samplerate),
                    samplerate=samplerate,
                    channels=1,
                    dtype='int16')
    sd.wait()

    # Save file
    write(filename, samplerate, frames)
    return os.path.abspath(filename)
