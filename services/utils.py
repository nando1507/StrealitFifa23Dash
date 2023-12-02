import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def FormataNumero(entrada:float):
    saida:str
    saida = format(entrada,"_.2f")
    return saida.replace(".",",").replace("_",".")

def ConsultaCotacaoMoeda():
    #Cotação Euro Atual
    url = 'https://www.google.com/search?client=firefox-b-d&q=converter+euro+para+real'
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"}
    page = requests.get(url,headers=header)
    bs = BeautifulSoup(page.content, 'html.parser')
    atributos = {'class':'DFlfde SwHCTb'}
    valor = bs.find_all("span", attrs=atributos)[0]

    return float(valor.text.replace(",","."))