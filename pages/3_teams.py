import streamlit as st
import pandas as pd

st.set_page_config(    
    page_title="Fifa Stats - Times",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.write("# Fifa 23")
st.write("## Times")


df = st.session_state["data"]
df_ligas = pd.read_csv("datasets\male_teams.csv", sep=",")


Ligas = st.sidebar.selectbox("Ligas", df_ligas["league_name"].unique())
df_times = df_ligas[df_ligas["league_name"] == Ligas]
Clubes = st.sidebar.selectbox("Clubes", df_times["team_name"].unique())

df[df["Club"] == Clubes]