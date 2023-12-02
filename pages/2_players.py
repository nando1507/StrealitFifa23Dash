import streamlit as st
from services import utils
import plotly.express as px
import plotly.graph_objects as go

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

ValorEuroParaReais = utils.ConsultaCotacaoMoeda()

df = st.session_state["data"]

Clubes = st.sidebar.selectbox("Clubes", df["PlayerClub"].unique())

df = df[df["PlayerClub"] == Clubes]
Jogadores = st.sidebar.selectbox("Jogador", df["PlayerName"].unique())
# Jogadores2 = st.sidebar.multiselect("Comparar", df["PlayerName"].unique())
# print(Jogadores2)
df_player = df[df["PlayerName"] == Jogadores]
df_player

#imagem
url_image = df_player["PlayerPhotoURL"].iloc[0]
st.image(url_image, width=50, use_column_width=False)
#Nome
Nome = df_player["PlayerName"].iloc[0]
st.title(f"{Nome}")

Clube = df_player["PlayerClub"].iloc[0]
LogoClube = df_player["PlayerClubFlagUrl"].iloc[0]
# <img  class="change-my-color" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/microsoftsqlserver/microsoftsqlserver-plain-wordmark.svg" width="40" height="40"/>
st.markdown(f"**Clube:** {Clube} ")
st.image(LogoClube, width=50, use_column_width=False)
Posicao = df_player["PlayerPosition"].iloc[0]
# Posicao = Posicao[str(Posicao).index(">")+1:]
st.markdown(f"**Posição:** {Posicao}")

col1, col2, col3, col4, col5 = st.columns(5)
Idade = df_player["PlayerAge"].iloc[0]
col1.markdown(f"**Idade:** {Idade}") 
Altura = 0 # df_player["Height(cm.)"].iloc[0]
# Altura = Altura.replace("cm","")
col2.markdown(f"**Altura:** {int(Altura) / 100} m") 
Peso = 0# df_player["Weight(lbs.)"].iloc[0]
col3.markdown(f"**Peso:** {Peso * 0.453:.2f} Kg") 
Nacionalidade = df_player["PlayerNationality"].iloc[0]
Bandeira = df_player["PlayerNationalityFlagUrl"].iloc[0]
col4.markdown(f"**Nacionalidade:** {Nacionalidade} ")
col4.image(
    Bandeira, width=50, use_column_width=False
#    use_container_width=True
)
NumeroCamisa = 0 # df_player["Kit Number"].iloc[0]
col5.markdown(f"**Camisa Nº:** {int(NumeroCamisa)} ")


st.divider()
Overall = int(df_player["PlayerOverall"].iloc[0])
Potential = int(df_player["PlayerOverall"].iloc[0])
# st.subheader(
st.metric(label="Overall", value=Overall, delta=Potential)
# )
st.progress(Overall)
st.progress(Potential, text="Potencial")

def FormataNumero(entrada:float):
    saida:str
    saida = format(entrada,"_.2f")
    return saida.replace(".",",").replace("_",".")

col5, col6, col7 = st.columns(3)
Value = 0 # df_player["Value(£)"].iloc[0]
col5.metric(label="Valor de Mercado Libras", value=f"£ {FormataNumero(Value)}") 
Wage = 0 #  df_player["Wage(£)"].iloc[0]
col6.metric(label="Remuneração Semanal Libras", value=f"£ {FormataNumero(Wage)}") 
Release_Clause = 0 #  df_player["Release Clause(£)"].iloc[0]
col7.metric(label="Clausula de Recisão Libras", value=f"£ {FormataNumero(Release_Clause)}") 

col8, col9, col10 = st.columns(3)
col8.metric(label="Valor de Mercado Reais", value=f"R$ {FormataNumero(Value * ValorEuroParaReais)}") 
col9.metric(label="Remuneração Semanal Reais", value=f"R$ {FormataNumero(Wage * ValorEuroParaReais)}") 
col10.metric(label="Clausula de Recisão Reais", value=f"R$ {FormataNumero(Release_Clause * ValorEuroParaReais)}")


PlayerPace = df_player["PlayerPace"].iloc[0]	
PlayerShooting = df_player["PlayerShooting"].iloc[0]	
PlayerPassing = df_player["PlayerPassing"].iloc[0]	
PlayerDribbling = df_player["PlayerDribbling"].iloc[0]	
PlayerDefending = df_player["PlayerDefending"].iloc[0]	
PlayerPhysicality = df_player["PlayerPhysicality"].iloc[0]

StatsName = ["Pace","Shooting","Passing","Dribbling","Defending","Physicality"]
StatsValues = [PlayerPace,PlayerShooting,PlayerPassing,PlayerDribbling,PlayerDefending,PlayerPhysicality]

fig = go.Figure()
fig = px.scatter_polar(r = StatsValues,
                        theta = StatsName,
                        # start_angle=90, 
                        # range_theta=[0,100],
                        fill = "toself",
                        name= Nome,
                        #mode = 'markers'
                    )

# fig2 = go.Figure()
fig2 = px.scatter_polar(r=range(0,90,10), 
                        theta=range(0,90,10),
                        range_theta=[0,90], 
                        start_angle=0, 
                        direction="counterclockwise")
col6.plotly_chart(fig2, theme="streamlit", use_container_width=True)

col5.plotly_chart(fig, theme="streamlit", use_container_width=True)