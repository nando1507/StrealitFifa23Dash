import streamlit as st
import pandas as pd
import plotly.express as px

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

df = df[df["Club"] == Clubes]

Colunas = [
    'Name', 
    'Age', 
    'Photo', 
    'Nationality', 
    'Flag', 
    'Overall', 
    'Potential',
    'Value(£)',
    'Wage(£)',
    'Release Clause(£)',
    'Club', 
    'Club Logo',     
    'Position', 
    'Height(cm.)', 
    'Weight(lbs.)', 
    'Kit Number'
]

# LogoClube = df["Club Logo"].iloc[0]
# st.image(LogoClube)
# clube = df["Club"].iloc[0]
# st.markdown(f"## {clube}")
df_cols = df[Colunas].set_index('Name')
st.dataframe(df_cols,
            column_config={
                "Overall": st.column_config.ProgressColumn("Overall", format="%d",min_value=0, max_value=100),
                "Potential": st.column_config.ProgressColumn("Potential", format="%d",min_value=0, max_value=100),
                "Value(£)": st.column_config.NumberColumn("Value(£)", format="$%d", min_value=0),
                "Wage(£)": st.column_config.ProgressColumn("Wage(£)", format="%f",min_value=0, max_value=df["Wage(£)"].max()),
                "Photo": st.column_config.ImageColumn("Photo", width="small"),
                "Flag": st.column_config.ImageColumn("Flag", width="small"),
                "Club Logo": st.column_config.ImageColumn("Club Logo", width="small"),
            })


fig_date = px.scatter(
    df_cols, 
    x="Position", 
    y="Age",
    color="Position",
    title="Idade por Posição",
    orientation="v"
)
st.plotly_chart(fig_date,use_container_width=True)


fig_date = px.line(
    df_cols, 
    x="Age", 
    y="Nationality",
    color="Nationality",
    title="Nacionalidade por Idade",
    orientation="v"
)
st.plotly_chart(fig_date,use_container_width=True)

st.button("Rerun")
