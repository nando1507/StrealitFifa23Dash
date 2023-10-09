import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(    
    page_title="Fifa Stats - Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)


def indexPos(entrada: str):
    try:
        return entrada[entrada.index(">")+1:]
        # print(entrada)
        #  return entrada
    except:
        print(f"erro: não definido")

df_fifa = pd.read_csv("datasets\FIFA23_official_data.csv",sep=",", index_col=0)
df_fifa = df_fifa.sort_values(by=["Overall","Age"], ascending=False)
df_fifa['Position'] = df_fifa['Position'].fillna("RES")
df_fifa['Position'] = df_fifa['Position'].apply(lambda x: indexPos(str(x)))

st.write("# Fifa 23 Official Dataset!")
# st.sidebar.markdown("https: /  / www.youtube.com / watch?v=0lYBYYHBT5k")
st.sidebar.markdown("Fernando Calo")
df_fifa

if "data" not in st.session_state:
    st.session_state["data"] = df_fifa


PosicoesColunas = ["Sigla","PosIngles","PosPortugues","Agrupamento"]
posicoes = [
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
    ["GK","Goalkeeper ","Goleiro","Defesa"],
    ["CF","Center Forward ","Segundo Atacante","Ataque"],
    ["ST","Striker ","CentroAvante","Ataque"],
    ["RM","Right Midfielder ","Meia Direito","Meio Campo"]
]

df_posicoes = pd.DataFrame(
    posicoes, columns=PosicoesColunas
)


Agrupamento = st.sidebar.selectbox("Categoria", df_posicoes["Agrupamento"].unique())
df = df_posicoes[df_posicoes["Agrupamento"] == Agrupamento]
Posicao = st.sidebar.selectbox("Posicao", df["PosPortugues"].unique())
df_filtro = df_posicoes[df_posicoes["Agrupamento"] == Agrupamento & df["PosPortugues"] == Posicao]
df_fifa = df_fifa[df_fifa["Position"]==df_filtro["Sigla"]]



fig_date = px.bar(
    df_fifa, 
    x="Age", 
    y="Nationality",
    color="Nationality",
    title="Faturamento por dia",
    orientation="v"
)
st.plotly_chart(fig_date,use_container_width=True)


st.button("Rerun")
