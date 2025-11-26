# pages/3_Record_Live_Meeting.py

import streamlit as st
from recorder import record_meeting, list_devices

st.title("Record Live Meeting Audio")

# Show device options
with st.expander("Available Audio Devices (Click to See)"):
    st.write(list_devices())

meet_link = st.text_input("Enter Meeting URL (optional)")

duration = st.slider("Recording Duration (seconds)", 10, 600, 60)

filename = st.text_input("Save audio as:", "meeting_recording.wav")

device_name = st.text_input(
    "Device Name (optional) — e.g., 'CABLE Output'",
    ""
)

if st.button("Start Recording"):
    with st.spinner("Recording... Please keep the meeting active"):
        try:
            path = record_meeting(
                meet_link=meet_link if meet_link else None,
                duration_seconds=duration,
                filename=filename,
                device_name=device_name if device_name else None
            )
            st.success(f"Recording saved: {path}")
        except Exception as e:
            st.error(f"Error: {e}")
