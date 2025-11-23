"""
recorder.py
------------
Record meeting audio (Google Meet, Zoom, Teams, etc.)
using VB-Audio Virtual Cable.

IMPORTANT:
◎ Windows Output  → CABLE Input
◎ Windows Input   → CABLE Output

If you want to hear audio while recording:
Control Panel → Recording → CABLE Output → Properties → Listen ⇒ ✔ Listen to this device
"""

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
import webbrowser
import os

def list_devices():
    """Return list of available audio devices (for debugging)."""
    return sd.query_devices()

def _set_vbcable():
    """Force sounddevice to use VB-Cable Output as the recording input."""
    device_name = "CABLE Output"  # must match VB-Audio Output name
    devices = sd.query_devices()
    idx = None

    for i, d in enumerate(devices):
        if device_name.lower() in d["name"].lower():
            idx = i
            break
    
    if idx is None:
        raise RuntimeError("VB-CABLE not found! Install and enable it first.\n"
                           "Check: https://vb-audio.com/Cable/")
    
    sd.default.device = idx  # set as input
    print(f"[INFO] Recording device set to: {devices[idx]['name']}")

def record_meeting(meet_link: str = None, duration_seconds: int = 60,
                   filename: str = "meeting_recording.wav",
                   samplerate: int = 16000):
    """
    Record audio from VB-Cable for a set duration.
    Optionally opens a meeting link before recording.

    Args:
        meet_link (str): Optional URL (Google Meet, Zoom, etc.)
        duration_seconds (int): Length of recording in seconds.
        filename (str): Output WAV file.
        samplerate (int): Sampling rate recommended for speech.

    Returns:
        str: Absolute path of saved WAV file.
    """

    # If link is provided, open in browser
    if meet_link:
        webbrowser.open(meet_link)
        time.sleep(4)  # wait for meeting to load

    # Force VB Cable device selection
    _set_vbcable()

    # Recording setup
    sd.default.samplerate = samplerate
    sd.default.channels = 1  # mono recommended for speech

    print(f"[INFO] Recording for {duration_seconds} seconds...")
    
    frames = sd.rec(int(duration_seconds * samplerate),
                    samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # wait till recording is finished

    # Ensure correct data type
    if frames.dtype != np.int16:
        frames = (frames * 32767).astype(np.int16)

    write(filename, samplerate, frames)
    print(f"[SUCCESS] Recording saved as {filename}")

    return os.path.abspath(filename)


# Debugging helper: print available devices if running standalone
if __name__ == "__main__":
    print("Available audio devices:")
    print(list_devices())
