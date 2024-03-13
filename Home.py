import streamlit as st
import sys
sys.path.append('modules')
from audiorecorder import audiorecorder
import uuid
from stt_and_weatherapi import *
import os


st.set_page_config(
    page_title="Vocal weather",
    page_icon="☁️",
)

if 'uuid' not in st.session_state:
    st.session_state['uuid']= str(uuid.uuid4())

st.title("Vocal weather")
st.text("⛈️ vs ☀️")

audio = audiorecorder("🎙️ Record", "🛑 Stop recording")

if len(audio) > 0 :
    audiofile=f"temp/audio{st.session_state['uuid']}.wav"
    audio.export(audiofile, format="wav")
    result=execute_cmd(audiofile)
    os.remove(audiofile)
    if result != None : st.text(result[2])
    else : st.text("Vous n'avez pas demandé la météo !")