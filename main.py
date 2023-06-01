from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import random

paginas = np.arange(1,5,50)
heads = {'Accept-Language':'pt-br,pt,q=0.8'}

titulos = []
anos = []
genero = []
duracao = []
votos = []
ratings = []
imdb_ratings = []
imdb_rates_std = []

for pagina in paginas:
    response = get("https://www.imdb.com/search/title/?genres=sci-fi&"
                   + "start=" + str(pagina) + "&explore=title_type,genres&ref_=adv_prv,", headers=heads)
# print (response)
    sleep(random.randint(8,16))
    if response.status_code != 200:
        warn(f'Solicitação {requests} retornou {response.status_code}')
    pagina_html = BeautifulSoup(response.text, 'html.parser')
# print (pagina_html)

    movie_containers = pagina_html.find_all('div', class_ = 'lister-item mode-advanced')
print(movie_containers)


