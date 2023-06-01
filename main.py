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
#captura titulo
    for container in movie_containers:
        if container.find('div', class_ = "ratings-metascore") is not None:
            title = container.h3.a.text
            titulos.append(title)
            #captura ano de lançamento
            if container.h3.find('span', class_ = 'lister-item-year text-muted unbold') is not None:
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                anos.append(year)
            else:
                anos.append(None)
            #captura nota 
            if container.p.find('span', class_ = 'certificate') is not None:
                rates = container.p.find('span', class_ = 'certificate').text
                ratings.append(rates)
            else:
                ratings.append(None)
            #captura genero
            if container.p.find('span', class_ = 'genre') is not None:
                genlis = container.p.find('span', class_ = 'genre').text.replace('/n','').strip().split(',')
                genero.append(genlis)
            else:
                genero.append(None)
            #captura duração
            if container.p.find('span', class_ = 'runtime') is not None:
                runt = int(container.p.find('span', class_ = 'runtime').text.replace(' min',''))
                duracao.append(runt)
            else:
                duracao.append(None)
            #captura avaliãção imdb
            if container.strong.text is not None:
                imdbv = float(container.strong.text.replace(',','.'))
                imdb_ratings.append(imdbv)
            else:
                imdb_ratings.append(None)
            #capturando votos
            if container.find('span', attrs = {'name':'nv'})['data-value']is not None:
                vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
                votos.append(vote)
            else:
                votos.append(None)            

listaFilme = pd.DataFrame({
    'Ano de lançamento':anos,
    'Título':titulos,
    'Duração':duracao,
    'Gênero':genero,    
    'Nota':ratings
})
listaFilme.loc[:,'Ano de Lançamento'] = listaFilme['Ano de lançamento'].str[-5:-1]

print (listaFilme)


