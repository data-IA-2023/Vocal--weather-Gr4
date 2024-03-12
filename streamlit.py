import streamlit as st
from audiorecorder import audiorecorder
import uuid
from teststt import *
import os

if 'uuid' not in st.session_state:
    st.session_state['uuid']= str(uuid.uuid4())


st.title("Vocal weather")

audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0 :
    audiofile=f"temp/audio{st.session_state['uuid']}.wav"
    audio.export(audiofile, format="wav")
    result=execute_cmd(audiofile)
    os.remove(audiofile)
    st.text(result)