import streamlit as st
from audiorecorder import audiorecorder
import uuid
import sys
sys.path.append('modules')
from stt_and_weatherapi import *
from read_db import *
import os
import io
import altair as alt


st.set_page_config(
    page_title="Vocal weather | Statistiques",
    page_icon="☁️",
)

st.title("Statistiques")
buf = io.StringIO()
df=read_db()
df.info(buf=buf)
st.text("Information sur la bdd :")
st.text("\n".join(buf.getvalue().split("\n")[1:-2]))
st.text("Scores des lieux :")

df_loc_mean=df.groupby('nlp_loc')['score_loc'].mean().reset_index()

chart = alt.Chart(df_loc_mean).mark_bar().encode(
    x='nlp_loc',
    y='score_loc',
)

st.altair_chart(chart, use_container_width=True)



st.text("Scores des dates :")

df_date_mean=df[df["nlp_date"]!=""][df["nlp_date"]!=None].groupby('nlp_date')['score_date'].mean().reset_index()

chart = alt.Chart(df_date_mean).mark_bar().encode(
    x='nlp_date',
    y='score_date',
)

st.altair_chart(chart, use_container_width=True)


satisfaction=len(df[df["feedback"]=="ok"]["feedback"])/len(df["feedback"])

st.text(f"Satisfaction des utilisateurs : {round(satisfaction*100,1)} %")