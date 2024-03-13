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

audio = audiorecorder("🎙️ Enregistrez votre voix", "🛑 C'est bon !")

if len(audio) > 0 :
    audiofile=f"temp/audio{st.session_state['uuid']}.wav"
    audio.export(audiofile, format="wav")
    result=execute_cmd(audiofile)
    os.remove(audiofile)
    if result == None : st.text("Vous n'avez pas demandé la météo !")
    else : 
        st.text(result[2])
        result=[e for e in result]
        feedback=st.empty()
        with feedback.container():
            ok = st.button("C'est bon !", help="Le service a fonctionné correctement.", args=(), kwargs={"bg_color": "green", "color": "green", "padding": "10px"})
            not_ok = st.button("Ca ne va pas !", help="Le service n'a pas fonctionné correctement.", args=(), kwargs={"bg_color": "red", "color": "red", "padding": "10px"})
            if ok:
                result[-1]="ok"
                add2db(result)
                feedback.empty()
            if not_ok:
                result[-1]="not ok"
                add2db(result)
                feedback.empty()