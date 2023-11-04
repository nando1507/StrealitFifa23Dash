import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import pyodbc
from sqlalchemy import create_engine

server = 'DESKTOP-UVIN3NU'
database = 'Particular'
username = 'sa'
password = '*casa123'

connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_string)
query = "SELECT *  FROM [Particular].[dbo].[Tb_EAFC_Players]"

df = pd.read_sql(query, engine)

st.set_page_config(    
    page_title="Fifa Stats - Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def FormataNumero(entrada:float):
    saida:str
    saida = format(entrada,"_.2f")
    return saida.replace(".",",").replace("_",".")

# df = pd.read_csv("datasets\CLEAN_FIFA23_official_data.csv",sep=",", index_col=0)
df = df.sort_values(by=["PlayerRank"])


df_fifa = df


PosicoesColunas = ["PlayerPosition","PosIngles","PosPortugues","Categoria"]
posicoes = [
    ["ALL","Todos","Todos","Todos"],
    ["CM","Central Midfielder ","Meio-campista","Meio Campo"],
    ["CB","Center Back ","Zagueiro","Defesa"],
    ["RWB","Right Midfielder ","Ala Direito","Defesa"],
    ["RW","Right Winger ","Ponta Direito","Ataque"],
    ["CDM","Central Defensive Midfielder ","Volante","Meio Campo"],
    ["LB","Left Back ","Lateral Esquerdo","Defesa"],
    ["LWB","Left Midfielder ","Ala Esquerdo","Defesa"],
    ["RB","Right Back ","Lateral Direito","Defesa"],
    ["CAM","Central Attacking Midfielder ","Meio-Atacante","Meio Campo"],
    ["LW","Left Winger ","Ponta Esquerdo","Ataque"],
    ["LM","Left Midfielder ","Meia Esquerdo","Meio Campo"],
    ["GK","Goalkeeper ","Goleiro","Goleiro"],
    ["CF","Center Forward ","Segundo Atacante","Ataque"],
    ["ST","Striker ","CentroAvante","Ataque"],
    ["RM","Right Midfielder ","Meia Direito","Meio Campo"]
]

df_posicoes = pd.DataFrame(
    posicoes, columns=PosicoesColunas
)
df_posicoes = df_posicoes.set_index("PlayerPosition")
df2 = df_posicoes

#Selectbox Categoria
Categoria = st.sidebar.selectbox("Categoria", df_posicoes["Categoria"].unique())

df_posicoes = df_posicoes[df_posicoes["Categoria"] == Categoria]
# print(df)
#Selectbox Posicao
if Categoria != "Todos":
    # print(Categoria)
    df_posicoes = df_posicoes[(df_posicoes["Categoria"] == Categoria)]
    df_posicoes.loc["ALL"] = ["Todos","Todos","Todos"]
    Posicao = st.sidebar.selectbox("Posicao", df_posicoes["PosPortugues"].unique())
else:
    Posicao = st.sidebar.selectbox("Posicao", df_posicoes["PosPortugues"].unique())

# df_fifa = df_fifa[df_fifa["Position"] == (df_posicoes[df_posicoes["PosPortugues"] == Posicao]) ]
# st.dataframe(df_posicoes)
if Posicao != "Todos":
    df_posicoes = df_posicoes[df_posicoes["PosPortugues"] == Posicao]
    # print(posicao)
else:
    df_fifa = df
    df_posicoes = df2
# print(df_posicoes)

df_fifa = pd.merge(df_fifa, df_posicoes, on='PlayerPosition', how='inner')
df_fifa = df_fifa.sort_values(by=["PlayerRank"])
    # df_fifa = df_fifa[df_posicoes_filtro["Sigla"] in df_fifa["Position"]]

slideMin = float(df_fifa["PlayerOverall"].min())
slideMax = float(df_fifa["PlayerOverall"].max())

values = st.slider('Selecione o Overall dos Atletas', slideMin - 5, 100.0, (slideMin, slideMax))
# print(values)

# if not values in (47.0, 91.0):
#     df_fifa = df_fifa[df_fifa["PlayerOverall"] in values]

st.write("# Fifa 23 Official Dataset!")
st.divider()
# st.sidebar.markdown("https://www.youtube.com/watch?v=0lYBYYHBT5k")


Colunas = [
    'PlayerName', 
    'PlayerAge', 
    'PlayerPhotoURL', 
    'PlayerPosition',
    'PlayerClub', 
    'PlayerClubFlagUrl',     
    'PlayerNationality', 
    'PlayerNationalityFlagUrl', 
    'PlayerOverall',
    'PlayerPace',
    'PlayerShooting',
    'PlayerPassing',
    'PlayerDribbling',
    'PlayerDefending',
    'PlayerPhysicality',
    'PlayerPreferredFoot',
    'PlayerAttWorkRate',
    'PlayerDefWorkRate',
    'PlayerSkillMoves',
    'PlayerWeakFoot',
]

st.sidebar.markdown("Fernando Calo")
df_cols = df_fifa[Colunas].set_index('PlayerName')
st.dataframe(df_cols,
            column_config={
                "PlayerName": st.column_config.TextColumn("Name", width="medium"), 
                "PlayerAge": st.column_config.TextColumn("Age", width="small"),
                "PlayerOverall": st.column_config.ProgressColumn("Overall", format="%d",min_value=0, max_value=100),
                "PlayerPace": st.column_config.ProgressColumn("Pace", format="%d",min_value=0, max_value=100),
                "PlayerShooting": st.column_config.ProgressColumn("Shooting", format="%d",min_value=0, max_value=100),
                "PlayerPassing": st.column_config.ProgressColumn("Passing", format="%d",min_value=0, max_value=100),
                "PlayerDribbling": st.column_config.ProgressColumn("Dribbling", format="%d",min_value=0, max_value=100),
                "PlayerDefending": st.column_config.ProgressColumn("Defending", format="%d",min_value=0, max_value=100),
                "PlayerPhysicality": st.column_config.ProgressColumn("Physicality", format="%d",min_value=0, max_value=100),
                "PlayerPhotoURL": st.column_config.ImageColumn("Photo", width="small"),
                "PlayerNationalityFlagUrl": st.column_config.ImageColumn("Flag", width="small"),
                "PlayerClubFlagUrl": st.column_config.ImageColumn("Club Logo", width="small"),
            })
st.divider()

if "data" not in st.session_state:
    st.session_state["data"] = df_fifa


#region Linha1
col1, col2 = st.columns(2)
df_GK = df_fifa[df_fifa["Categoria"] == "Goleiro"].groupby(by=["PlayerAge","PlayerPosition"])[["PlayerRank"]].count().reset_index()
fig_date_GK = px.bar(
    df_GK,
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Idade Goleiros",
    orientation="v"
)

fig_date_Gk_area = px.area(
    df_GK, 
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Agrupamento",
    orientation="v"
)

col1.plotly_chart(fig_date_GK,use_container_width=True)
col2.plotly_chart(fig_date_Gk_area,use_container_width=True)
# col2.area_chart(df_GK, x="PlayerAge", y="PlayerRank", color="PlayerPosition",use_container_width=True)
#endregion
st.divider()
#region Linha2
col3, col4 = st.columns(2)
df_defesa = df_fifa[df_fifa["Categoria"] == "Defesa"].groupby(by=["PlayerAge","PlayerPosition"])[["PlayerRank"]].count().reset_index()
fig_date_defesa = px.bar(
    df_defesa, 
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Idade Defesa",
    orientation="v"
)
fig_date_defesa_area = px.area(
    df_defesa, 
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Agrupamento",
    orientation="v"
)
col3.plotly_chart(fig_date_defesa,use_container_width=True)
col4.plotly_chart(fig_date_defesa_area,use_container_width=True)
#col4.area_chart(df_defesa, x="PlayerAge", y="PlayerRank", color="PlayerPosition",use_container_width=True)
#endregion
st.divider()
#region Linha3
col5, col6 = st.columns(2)
df_Meio = df_fifa[df_fifa["Categoria"] == "Meio Campo"].groupby(by=["PlayerAge","PlayerPosition"])[["PlayerRank"]].count().reset_index()
fig_date_meio = px.bar(
    df_Meio, 
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Idade Meio Campistas",
    orientation="v"
)

fig_scatter = px.scatter(
    df_Meio,
    x="PlayerAge",
    y="PlayerPosition",
    size="PlayerRank",
    color="PlayerRank",
    title="Agrupamento"
)


col5.plotly_chart(fig_date_meio,use_container_width=True)
col6.plotly_chart(fig_scatter, use_container_width=True)
# col6.scatter_chart(df_Meio,
#     x="PlayerAge",
#     y="PlayerPosition",
#     color="PlayerRank", 
#     size="PlayerRank",
#     use_container_width=True
# )
#endregion
st.divider()
#region Linha4
col7, col8 = st.columns(2)
df_Ataque = df_fifa[df_fifa["Categoria"] == "Ataque"].groupby(by=["PlayerAge","PlayerPosition"])[["PlayerRank"]].count().reset_index()
fig_date_Ataque = px.bar(
    df_Ataque, 
    x="PlayerAge", 
    y="PlayerRank",
    color="PlayerPosition",
    title="Idade Atacantes",
    orientation="v"
)

fig_date_Bolha = px.scatter(
    df_Ataque, 
    x="PlayerAge",
    y="PlayerRank",
    size="PlayerRank",
    color="PlayerPosition",
    hover_name="PlayerPosition",
    title="Agrupamento",
    orientation="v"
)


col7.plotly_chart(fig_date_Ataque,use_container_width=True)


col8.plotly_chart(fig_date_Bolha,use_container_width=True)
#endregion
st.divider()

df_MediaOverall =  df_fifa.groupby(by=["PlayerAge","PlayerPosition"])[["PlayerOverall"]].mean().reset_index().round(2)
df_QtdeOverall =  df_fifa.groupby(by=["PlayerAge","PlayerPosition"])[["PlayerOverall"]].count().reset_index()
df_Overall = pd.merge(df_MediaOverall, df_QtdeOverall, on=["PlayerAge","PlayerPosition"], how='inner')

fig_Overall = px.scatter(
    df_Overall,
    x="PlayerOverall_x",
    y="PlayerAge",
    color="PlayerPosition",
    size="PlayerOverall_y"

)


st.plotly_chart(fig_Overall, use_container_width=True)

st.button("Rerun")
