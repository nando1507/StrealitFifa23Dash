import pandas as pd
import numpy as np
import pyodbc
# import openpyxl
from sqlalchemy import create_engine

def __Conexao():
    server = 'DESKTOP-UVIN3NU'
    database = 'Particular'
    username = 'sa'
    password = '*casa123'
    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    return engine

def CarregaDatasetJogadores():    
    query = "SELECT *  FROM [Particular].[dbo].[Tb_EAFC_Players] With (Nolock)"
    df = pd.read_sql(query, __Conexao())
    df = df.sort_values(by=["PlayerRank"])
    return df
    

def CarregaDatasetPosicoes():
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

    return df_posicoes

def CarregaDatasetEstilos():
    query = "SELECT *  FROM [Particular].[dbo].[Tb_EAFC_Styles] With (Nolock)"
    df_Styles = pd.read_sql(query, __Conexao())
    return df_Styles

