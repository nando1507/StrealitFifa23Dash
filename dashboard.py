import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth
from services import DatasetService, utils
import pandas as pd

def Dashboard():
    df_Styles = DatasetService.CarregaDatasetEstilos()
    df = DatasetService.CarregaDatasetJogadores()  
    df_posicoes = DatasetService.CarregaDatasetPosicoes()
    df2 = df_posicoes
    df_fifa = df

    Categoria = st.sidebar.selectbox("Categoria", df_posicoes["Categoria"].unique())

    df_posicoes = df_posicoes[df_posicoes["Categoria"] == Categoria]
    
    #Selectbox Posicao
    if Categoria != "Todos":
        # print(Categoria)
        df_posicoes = df_posicoes[(df_posicoes["Categoria"] == Categoria)]
        df_posicoes.loc["ALL"] = ["Todos","Todos","Todos"]
        Posicao = st.sidebar.selectbox("Posicao", df_posicoes["PosPortugues"].unique())
    else:
        Posicao = st.sidebar.selectbox("Posicao", df_posicoes["PosPortugues"].unique())

    if Posicao != "Todos":
        df_posicoes = df_posicoes[df_posicoes["PosPortugues"] == Posicao]        
    else:
        df_fifa = df
        df_posicoes = df2    

    df_fifa = pd.merge(df_fifa, df_posicoes, on='PlayerPosition', how='inner')
    df_fifa = df_fifa.sort_values(by=["PlayerRank"])
    df_fifa_Export = df_fifa.set_index("PlayerRank")
    try:
        df_fifa_Export.to_csv('datasets/EAFC24_Dados.csv', encoding='UTF-8')
        df_fifa_Export.to_excel('datasets/EAFC24_Dados.xlsx')
        df_Styles.to_csv('datasets/EAFC24_Dados_Estilos.csv', encoding='UTF-8')        
        df_Styles.to_excel('datasets/EAFC24_Dados_Estilos.xlsx')
    except:
        st.exception("Erro ao exportar o Dataset")


    for index, valor in enumerate(df_fifa_Export.columns):
        df_fifa_Export.drop(valor, axis="columns")
        # df_fifa = df_fifa[df_posicoes_filtro["Sigla"] in df_fifa["Position"]]

    slideMin = float(df_fifa["PlayerOverall"].min())
    slideMax = float(df_fifa["PlayerOverall"].max())

    values = st.slider('Selecione o Overall dos Atletas', slideMin - 5, 100.0, (slideMin, slideMax))

    st.write("# Fifa 23 Official Dataset!")
    st.divider()

    with st.expander("Cores de exibição"):
        colColor1, colColor2 = st.columns(2)
        colorA = colColor1.color_picker('Cor Primária', '#2980B9')
        colorb = colColor2.color_picker('Cor Secundária', '#C0392B')

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
                    "PlayerOverall": st.column_config.ProgressColumn("Overall",format="%d",min_value=0, max_value=100), #color=colorA,
                    "PlayerPace": st.column_config.ProgressColumn("Ritmo", format="%d",min_value=0, max_value=100),
                    "PlayerShooting": st.column_config.ProgressColumn("Finalização", format="%d",min_value=0, max_value=100),
                    "PlayerPassing": st.column_config.ProgressColumn("Passe", format="%d",min_value=0, max_value=100),
                    "PlayerDribbling": st.column_config.ProgressColumn("Drible", format="%d",min_value=0, max_value=100),
                    "PlayerDefending": st.column_config.ProgressColumn("Defesa", format="%d",min_value=0, max_value=100),
                    "PlayerPhysicality": st.column_config.ProgressColumn("Físico", format="%d",min_value=0, max_value=100),
                    "PlayerPhotoURL": st.column_config.ImageColumn("Foto", width="small"),
                    "PlayerPosition": st.column_config.TextColumn("Posição", width="30px"),
                    "PlayerNationality": st.column_config.TextColumn("Nacionalidade"),
                    "PlayerNationalityFlagUrl": st.column_config.ImageColumn("Bandeira", width="small"),
                    "PlayerClubFlagUrl": st.column_config.ImageColumn("Clube Logo", width="50px"),
                    "PlayerClub": st.column_config.TextColumn("Clube"),
                    "PlayerPreferredFoot": st.column_config.TextColumn("Pé Preferido"), #, format="%d ⭐",),
                    "PlayerWeakFoot": st.column_config.TextColumn("Pé Ruim"), #, format="%d ⭐",),
                    "PlayerAttWorkRate": st.column_config.TextColumn("Rating de Ataque"),
                    "PlayerDefWorkRate": st.column_config.TextColumn("Rating de Defesa"),
                    "PlayerSkillMoves": st.column_config.TextColumn("Movimento"),
                }, use_container_width=True)
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

    df_MediaOverall = df_fifa.groupby(by=["PlayerAge","PlayerPositionPT"])[["PlayerOverall"]].mean().reset_index().round(2)
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

    st.divider()

    df_resumoJogadores = df[['PlayerRank','PlayerName','PlayerPosition']]
    df_JogadoresEstilos = pd.merge(df_resumoJogadores, df_Styles, on=["PlayerRank"], how='inner')

    colEstilo1, colEstilo2 = st.columns(2)

    colEstilo1.dataframe(df_JogadoresEstilos,
        column_config={
            "PlayerName": st.column_config.TextColumn("Nome"), 
            "PlayerPosition": st.column_config.TextColumn("Posição"),
            "StyleName": st.column_config.TextColumn("Estilo"),
            "StyleURLImg": st.column_config.ImageColumn("Foto", width="small"),
            "CdStyleTipo": st.column_config.TextColumn("Codigo de Estilo"),
            "NomeStyleTipo": st.column_config.TextColumn("Tipo de Estilo"),
        }     
        ,use_container_width=True   
    )

    estilos_Agg = df_JogadoresEstilos.groupby(by=["StyleName","NomeStyleTipo","PlayerPosition"])[["PlayerName"]].count().reset_index()
    estilos_Qtde = df_JogadoresEstilos.groupby(by=["StyleName","NomeStyleTipo"])[["PlayerName"]].count().reset_index()
    tabEstilo1, tabEstilo2, tabEstilo3, tabEstilo4 = colEstilo2.tabs(["Geral", "Plus", "Comum", "Linhas"])

    fig_style = px.scatter(
        estilos_Agg,
        x="StyleName",
        y="PlayerPosition",
        color="NomeStyleTipo",
        size="PlayerName",
        # symbol="PlayerPosition",
        hover_data=['PlayerName']
    )
    tabEstilo1.plotly_chart(fig_style, use_container_width=True)

    fig_style1 = px.scatter(
        estilos_Agg[estilos_Agg["NomeStyleTipo"] == "Plus"],
        x="StyleName",
        y="PlayerPosition",
        color="NomeStyleTipo",
        size="PlayerName",
        # symbol="PlayerPosition",
        hover_data=['PlayerName']
    )
    tabEstilo2.plotly_chart(fig_style1, use_container_width=True)


    fig_style2 = px.scatter(
        estilos_Agg[estilos_Agg["NomeStyleTipo"] == "Simple"],
        x="StyleName",
        y="PlayerPosition",
        color="NomeStyleTipo",
        size="PlayerName",
        # symbol="PlayerPosition",
        hover_data=['PlayerName']
    )
    tabEstilo3.plotly_chart(fig_style2, use_container_width=True)

    fig_style0 = px.line(
        estilos_Qtde,
        x="StyleName",
        y="PlayerName",
        color="NomeStyleTipo"        
    )
    tabEstilo4.plotly_chart(fig_style0, use_container_width=True)