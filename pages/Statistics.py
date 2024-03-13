import streamlit as st
from audiorecorder import audiorecorder
import uuid
from teststt import *
import os


st.set_page_config(
    page_title="Vocal weather-Statistics",
    page_icon="☁️",
)

if 'uuid' not in st.session_state:
    st.session_state['uuid']= str(uuid.uuid4())

st.title("Vocal weather")