import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(    
    page_title="Fifa Stats - Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

df_fifa = pd.read_csv("datasets\FIFA23_official_data.csv",sep=",", index_col=0)
df_fifa = df_fifa.sort_values(by=["Overall","Age"], ascending=False)

st.write("# Fifa 23 Official Dataset!")
# st.sidebar.markdown("https://www.youtube.com/watch?v=0lYBYYHBT5k")
st.sidebar.markdown("Fernando Calo")

if "data" not in st.session_state:
    st.session_state["data"] = df_fifa


df_fifa

st.button("Rerun")