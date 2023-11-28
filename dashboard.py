import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import pyodbc
import openpyxl
from sqlalchemy import create_engine
import streamlit_authenticator as stauth


st.set_page_config(    
    page_title="Fifa Stats - Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def FormataNumero(entrada:float):
    saida:str
    saida = format(entrada,"_.2f")
    return saida.replace(".",",").replace("_",".")

def Dashboard():
    server = 'DESKTOP-UVIN3NU'
    database = 'Particular'
    username = 'sa'
    password = '*casa123'

    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    query = "SELECT *  FROM [Particular].[dbo].[Tb_EAFC_Players] With (Nolock)"
    query2 = "SELECT *  FROM [Particular].[dbo].[Tb_EAFC_Styles] With (Nolock)"

    df = pd.read_sql(query, engine)
    df_Styles = pd.read_sql(query2, engine)

    # df = pd.read_csv("datasets\CLEAN_FIFA23_official_data.csv",sep=",", index_col=0)
    df = df.sort_values(by=["PlayerRank"])

    df_fifa = df

    PosicoesColunas = ["PlayerPosition","PlayerPositionPT","PosIngles","PosPortugues","Categoria"]
    posicoes = [
        ["ALL","All","Todos","Todos","Todos"],
        ["CM","MC","Central Midfielder ","Meia Central","Meio Campo"],
        ["CB","ZAG","Center Back ","Zagueiro","Defesa"],
        ["RWB","ALD","Right Midfielder ","Ala Direito","Defesa"],
        ["RW","PD","Right Winger ","Ponta Direito","Ataque"],
        ["CDM","VOL","Central Defensive Midfielder ","Volante","Meio Campo"],
        ["LB","LE","Left Back ","Lateral Esquerdo","Defesa"],
        ["LWB","ALE","Left Midfielder ","Ala Esquerdo","Defesa"],
        ["RB","LD","Right Back ","Lateral Direito","Defesa"],
        ["CAM","MEI","Central Attacking Midfielder ","Meio-Atacante","Meio Campo"],
        ["LW","PE","Left Winger ","Ponta Esquerdo","Ataque"],
        ["LM","ME","Left Midfielder ","Meia Esquerdo","Meio Campo"],
        ["GK","GOL","Goalkeeper ","Goleiro","Goleiro"],
        ["CF","SA","Center Forward ","Segundo Atacante","Ataque"],
        ["ST","ATA","Striker ","CentroAvante","Ataque"],
        ["RM","MD","Right Midfielder ","Meia Direito","Meio Campo"]
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
    df_fifa_Export = df_fifa.set_index("PlayerRank")
    df_fifa_Export.to_csv('datasets/EAFC24_Dados.csv', encoding='UTF-8')
    df_fifa_Export.to_excel('datasets/EAFC24_Dados.xlsx')

    for index, valor in enumerate(df_fifa_Export.columns):
        df_fifa_Export.drop(valor, axis="columns")
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

    
    df_cols = df_fifa[Colunas].set_index('PlayerName')
    st.dataframe(df_cols,
                column_config={
                    "PlayerName": st.column_config.TextColumn("Nome"), 
                    "PlayerAge": st.column_config.TextColumn("Idade", width="small"),
                    "PlayerOverall": st.column_config.ProgressColumn("Overall", format="%d",min_value=0, max_value=100),
                    "PlayerPace": st.column_config.ProgressColumn("Ritmo", format="%d",min_value=0, max_value=100),
                    "PlayerShooting": st.column_config.ProgressColumn("Finalização", format="%d",min_value=0, max_value=100),
                    "PlayerPassing": st.column_config.ProgressColumn("Passe", format="%d",min_value=0, max_value=100),
                    "PlayerDribbling": st.column_config.ProgressColumn("Drible", format="%d",min_value=0, max_value=100),
                    "PlayerDefending": st.column_config.ProgressColumn("Defesa", format="%d",min_value=0, max_value=100),
                    "PlayerPhysicality": st.column_config.ProgressColumn("Físico", format="%d",min_value=0, max_value=100),
                    "PlayerPhotoURL": st.column_config.ImageColumn("Foto", width="small"),
                    "PlayerPosition": st.column_config.TextColumn("Posição", width="small"),
                    "PlayerNationality": st.column_config.TextColumn("Nacionalidade"),
                    "PlayerNationalityFlagUrl": st.column_config.ImageColumn("Bandeira", width="small"),
                    "PlayerClubFlagUrl": st.column_config.ImageColumn("Clube Logo", width="small"),
                    "PlayerClub": st.column_config.TextColumn("Clube"),
                    "PlayerPreferredFoot": st.column_config.TextColumn("Pé Preferido"),
                    "PlayerWeakFoot": st.column_config.TextColumn("Pé Ruim"),
                    "PlayerAttWorkRate": st.column_config.TextColumn("Rating de Ataque"),
                    "PlayerDefWorkRate": st.column_config.TextColumn("Rating de Defesa"),
                    "PlayerSkillMoves": st.column_config.TextColumn("Movimento"),
                })
    st.divider()

    if "data" not in st.session_state:
        st.session_state["data"] = df_fifa

    tab1, tab2, tab3, tab4 = st.tabs(["Goleiros", "Defensores", "Meio Campistas", "Atacantes"])

    with tab1:
        #region Linha1
        col1, col2 = st.columns(2)
        df_GK = df_fifa[df_fifa["Categoria"] == "Goleiro"].groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerRank"]].count().reset_index()
        fig_date_GK = px.bar(
            df_GK,
            x="PlayerAge", 
            y="PlayerRank",
            color="PlayerPositionPT",
            title="Idade Goleiros",
            orientation="v"
        )

        fig_date_Gk_area = px.scatter(
            df_GK, 
            x="PlayerAge",
            y="PlayerRank",
            size="PlayerRank",
            hover_name="PlayerPositionPT",
            color="PlayerPositionPT",
            title="Agrupamento"
        )

        col1.plotly_chart(fig_date_GK,use_container_width=True)
        col2.plotly_chart(fig_date_Gk_area,use_container_width=True)
        # col2.area_chart(df_GK, x="PlayerAge", y="PlayerRank", color="PlayerPosition",use_container_width=True)
        #endregion
        st.divider()

    with tab2:
        #region Linha2
        col3, col4 = st.columns(2)
        df_defesa = df_fifa[df_fifa["Categoria"] == "Defesa"].groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerRank"]].count().reset_index()
        fig_date_defesa = px.bar(
            df_defesa, 
            x="PlayerAge", 
            y="PlayerRank",
            color="PlayerPositionPT",
            title="Idade Defesa",
            orientation="v"
        )
        fig_date_defesa_area = px.scatter(
            df_defesa, 
            x="PlayerAge",
            y="PlayerRank",
            size="PlayerRank",
            hover_name="PlayerPositionPT",
            color="PlayerPositionPT",
            title="Agrupamento"
        )
        col3.plotly_chart(fig_date_defesa,use_container_width=True)
        col4.plotly_chart(fig_date_defesa_area,use_container_width=True)
        # col4.area_chart(df_defesa, x="PlayerAge", y="PlayerRank", color="PlayerPosition",use_container_width=True)
        #endregion
        st.divider()

    with tab3:
        #region Linha3
        col5, col6 = st.columns(2)
        df_Meio = df_fifa[df_fifa["Categoria"] == "Meio Campo"].groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerRank"]].count().reset_index()
        fig_date_meio = px.bar(
            df_Meio, 
            x="PlayerAge", 
            y="PlayerRank",
            color="PlayerPositionPT",
            title="Idade Meio Campistas",
            orientation="v"
        )

        fig_scatter = px.scatter(
            df_Meio,
            x="PlayerAge",
            y="PlayerRank",
            size="PlayerRank",
            hover_name="PlayerPositionPT",
            color="PlayerPositionPT",
            title="Agrupamento"
        )


        col5.plotly_chart(fig_date_meio,use_container_width=True)
        col6.plotly_chart(fig_scatter, use_container_width=True)
        #endregion
        st.divider()

    with tab4:
        #region Linha4
        col7, col8 = st.columns(2)
        df_Ataque = df_fifa[df_fifa["Categoria"] == "Ataque"].groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerRank"]].count().reset_index()
        fig_date_Ataque = px.bar(
            df_Ataque, 
            x="PlayerAge", 
            y="PlayerRank",
            color="PlayerPositionPT",
            title="Idade Atacantes",
            orientation="v"
        )

        fig_date_Bolha = px.scatter(
            df_Ataque, 
            x="PlayerAge",
            y="PlayerRank",
            size="PlayerRank",
            color="PlayerPositionPT",
            hover_name="PlayerPositionPT",
            title="Agrupamento",
            orientation="v"
        )


        col7.plotly_chart(fig_date_Ataque,use_container_width=True)
        col8.plotly_chart(fig_date_Bolha,use_container_width=True)
        #endregion
        st.divider()


    df_MediaOverall =  df_fifa.groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerOverall"]].mean().reset_index().round(2)
    df_MediaOverall.rename(columns={"PlayerOverall": "MediaOverall"}, inplace=True)
    df_QtdeOverall =  df_fifa.groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerOverall"]].count().reset_index()
    df_QtdeOverall.rename(columns={"PlayerOverall": "QuantidadeOverall"}, inplace=True)
    df_Overall = pd.merge(df_MediaOverall, df_QtdeOverall, on=["PlayerAge","PlayerPositionPT"], how='inner')

    fig_Overall = px.scatter(
        df_Overall,
        x="MediaOverall",
        y="PlayerAge",
        color="PlayerPositionPT",
        size="QuantidadeOverall"
    )
    st.plotly_chart(fig_Overall, use_container_width=True)


