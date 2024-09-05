import requests 
from bs4 import BeautifulSoup
from urllib.parse import unquote
from utils.constants import ALLOWED_FORMATS
from utils.utils import check_if_html_is_valid_to_get_media_links

def get_links_of_html(html):
    """
    Extract links of the episodes from the given HTML content.

    Args:
        html (str): The HTML content as a string.

    Returns:
        list: A list of links to the episodes.
    """
    soup = BeautifulSoup(html, features="lxml")
    tags = soup("a")
    links = []
    for tag in tags:
        link = tag.get("href")
        if link[-3:len(link)] in ALLOWED_FORMATS:
            if str(link).find("\\") != -1:
                link = str(link).replace("\\","")
            links.append(link)
    return links 

def scrapping(URL_SERIE, CARPETA_DESTINO, verify = True):
    """
    Scrape all links contained in the series folder and save them to files.

    Args:
        URL_SERIE (str): The URL of the series folder.
        CARPETA_DESTINO (str): The destination folder path to save the links.
    """
    # Get all links contained in the series folder
    serie = requests.get(URL_SERIE, verify = verify)
    soup = BeautifulSoup(serie.content, features="lxml")
    tags = soup("a")
    links = []
    for tag in tags[5:len(tags)]:
        links.append(tag.get('href'))

    for link in links:
        res = requests.get(f"{URL_SERIE}{link}") 
        # Check if it is a folder containing a season
        try:
            if check_if_html_is_valid_to_get_media_links(res.headers['content-type']):
                # Extract links of the episodes
                content_links = get_links_of_html(str(res.content)) 
                # Open the file to save the links
                nombre_archivo = unquote(link[0:len(link) - 1])
                file = open(f"{CARPETA_DESTINO}/{nombre_archivo}.txt", "w", encoding="utf-8")
                # Save the episode links to the file
                for content in content_links:
                    file.write(f"{res.url}{content}\n") 
        except:
            continue            
                
def get_one_temp(URL_TEMP, CARPETA_DESTINO, verify = True):
    """
    Get the links of one season and save them to a file.

    Args:
        URL_TEMP (str): The URL of the season.
        CARPETA_DESTINO (str): The destination folder path to save the links.
    """
    html_temp = requests.get(URL_TEMP, verify=verify).content 
    content_links = get_links_of_html(str(html_temp)) 
    # Open the file to save the links
    nombre_archivo = str(unquote(URL_TEMP)).split("/")[-1]
    file = open(f"{CARPETA_DESTINO}/{nombre_archivo}.txt", "w", encoding="utf-8")
    # Save the episode links to the file
    for content in content_links:
        file.write(f"{URL_TEMP}/{content}\n")
