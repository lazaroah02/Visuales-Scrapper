import requests 
from bs4 import BeautifulSoup
from urllib.parse import unquote
from constants import ALLOWED_FORMATS
from utils import check_if_html_is_valid_to_get_media_links

#function that take a html code  and extract the links of the episodes inside
def get_links_of_html(html):
    soup =  BeautifulSoup(html, features="lxml")
    tags = soup("a")
    links = []
    for tag in tags:
        link = tag.get("href")
        if link[-3:len(link)] in ALLOWED_FORMATS:
            if str(link).find("\\") != -1:
                link = str(link).replace("\\","")
            links.append(link)
    return links 

def scrapping(URL_SERIE, CARPETA_DESTINO):
    #obtengo todos los links que contiene la carpeta de la serie
    serie = requests.get(URL_SERIE)
    soup =  BeautifulSoup(serie.content, features="lxml")
    tags = soup("a")
    links = []
    for tag in tags[5:len(tags)]:
        links.append(tag.get('href'))

    for link in links:
        res = requests.get(f"{URL_SERIE}{link}") 
        #compruebo que sea una carpeta que contenga una temporada
        try:
            if check_if_html_is_valid_to_get_media_links(res.headers['content-type']):
                # extraigo los links de los capitulos
                content_links = get_links_of_html(str(res.content)) 
                #abro el archivo donde se guardaran los links
                nombre_archivo = unquote(link[0:len(link) - 1])
                file = open(f"{CARPETA_DESTINO}/{nombre_archivo}.txt", "w", encoding="utf-8")
                #guardo los links de los capitulos en el archivo
                for content in content_links:
                    file.write(f"{res.url}{content}\n") 
        except:
            continue            
                
def get_one_temp(URL_TEMP, CARPETA_DESTINO):
    html_temp = requests.get(URL_TEMP).content 
    content_links = get_links_of_html(str(html_temp)) 
    #abro el archivo donde se guardaran los links
    nombre_archivo = str(unquote(URL_TEMP)).split("/")[-1]
    file = open(f"{CARPETA_DESTINO}/{nombre_archivo}.txt", "w", encoding="utf-8")
    #guardo los links de los capitulos en el archivo
    for content in content_links:
        file.write(f"{URL_TEMP}/{content}\n")      
