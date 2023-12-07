import os
import pandas as pd
from services import DatasetService as dss

def ListaPasta(caminho:str):
    list = {}
    for p, _, files in os.walk(os.path.abspath(caminho)):
        for file in files:
            list[file] = "'" +  os.path.join(p, file).replace('\\', '/') + "'"
    
    # print(list)
    return list

listagem = ListaPasta("C:/Users/nando/Desktop/Python/Dashboard Streamlit Times/datasets")
for k, v in listagem.items():
    dss.CarregaTXTDatasetSQL(v.value(), sep=",", k)