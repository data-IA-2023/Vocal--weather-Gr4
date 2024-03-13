import streamlit as st
from audiorecorder import audiorecorder
import uuid
import sys
sys.path.append('modules')
from stt_and_weatherapi import *
import os


st.set_page_config(
    page_title="Vocal weather-Statistics",
    page_icon="☁️",
)

if 'uuid' not in st.session_state:
    st.session_state['uuid']= str(uuid.uuid4())

st.title("Statistics")