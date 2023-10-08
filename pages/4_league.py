import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(    
    page_title="Fifa Stats - Ligas",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })


st.write("# Fifa 23")
st.write("## Ligas")

df_ligas = pd.read_csv("datasets\male_teams.csv", sep=",")

Ligas = st.sidebar.selectbox("Ligas", df_ligas["league_name"].unique())
df_ligas = df_ligas[df_ligas["league_name"] == Ligas]
Pais = st.sidebar.selectbox("Pais", df_ligas["nationality_name"].unique())
df_ligas