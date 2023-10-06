import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(    
    page_title="DashVendas",
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
df_fifa