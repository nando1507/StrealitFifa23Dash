import streamlit as st
from PIL import Image

st.set_page_config(    
    page_title="Fifa Stats - Jogadores",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.write("# Fifa 23")
st.write("## Jogadores")


df = st.session_state["data"]

Clubes = st.sidebar.selectbox("Clubes", df["Club"].unique())

df = df[df["Club"] == Clubes]
Jogadores = st.sidebar.selectbox("Jogador", df["Name"].unique())

df_player = df[df["Name"] == Jogadores]
df_player

#imagem
url_image = df_player["Photo"].iloc[0]
st.image(url_image#,/*use_container_width=True
        )

#Nome
Nome = df_player["Name"].iloc[0]
st.title(f"{Nome}")

Clube = df_player["Club"].iloc[0]
LogoClube = df_player["Club Logo"].iloc[0]
# <img  class="change-my-color" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/microsoftsqlserver/microsoftsqlserver-plain-wordmark.svg" width="40" height="40"/>
st.markdown(f"**Clube:** {Clube} ")
st.image(LogoClube)
Posicao = df_player["Position"].iloc[0]
Posicao = Posicao[str(Posicao).index(">")+1:]
st.markdown(f"**Posição:** {Posicao}")

col1, col2, col3, col4, col5 = st.columns(5)
Idade = df_player["Age"].iloc[0]
col1.markdown(f"**Idade:** {Idade}") 
Altura = df_player["Height"].iloc[0]
Altura = Altura.replace("cm","")
col2.markdown(f"**Altura:** {int(Altura) / 100}m") 
Peso = df_player["Weight"].iloc[0]
col3.markdown(f"**Peso:** {Peso}") 
Nacionalidade = df_player["Nationality"].iloc[0]
Bandeira = df_player["Flag"].iloc[0]
col4.markdown(f"**Nacionalidade:** {Nacionalidade} ")
col4.image(
    Bandeira,
#    use_container_width=True
)
NumeroCamisa = df_player["Kit Number"].iloc[0]
col5.markdown(f"**Camisa Nº:** {int(NumeroCamisa)} ")


st.divider()
Overall = int(df_player["Overall"].iloc[0])
Potential = int(df_player["Potential"].iloc[0])
# st.subheader(
st.metric(label="Overall", value=Overall, delta=Potential)
# )
st.progress(Overall)
st.progress(Potential, text="Potencial")


col5, col6, col7 = st.columns(3)
Value = df_player["Value"].iloc[0]
col5.metric(label="Valor de Mercado", value=f"{Value}") 
Wage = df_player["Wage"].iloc[0]
col6.metric(label="Remuneração Semanal", value=f"{Wage}") 
Release_Clause = df_player["Release Clause"].iloc[0]
col7.metric(label="Clausula de Recisão", value=f"{Release_Clause}",) 
