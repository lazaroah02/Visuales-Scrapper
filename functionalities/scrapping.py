import requests 
from bs4 import BeautifulSoup
from urllib.parse import unquote
from utils.constants import ALLOWED_FORMATS
from utils.utils import check_if_html_is_valid_to_get_media_links, format_key_name

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
        if str(link[-3:len(link)]).lower() in ALLOWED_FORMATS:
            if str(link).find("\\") != -1:
                link = str(link).replace("\\","")
            links.append(link)
    return links 

def scrapping(URL_SERIE, verify = True):
    """
    Scrape all links contained in the series folder and save them to files.

    Args:
        URL_SERIE (str): The URL of the series folder.
        CARPETA_DESTINO (str): The destination folder path to save the links.
    """
    if not str(URL_SERIE).endswith("/"):
        URL_SERIE += "/"
        
    serie_name = format_key_name(str(URL_SERIE).split('/')[-2])
    scrapping_result = {serie_name:{}}
    
    # Get all links contained in the series folder
    serie = requests.get(URL_SERIE, verify = verify)
    soup = BeautifulSoup(serie.content, features="lxml")
    tags = soup("a")
    links = []
    for tag in tags[5:len(tags)]:
        links.append(tag.get('href'))
    
    #iterate all the seasons
    for link in links:
        temp_name = format_key_name(link)
        scrapping_result[serie_name][temp_name] = []
        res = requests.get(f"{URL_SERIE}{link}") 
        # Check if it is a folder containing a season
        try:
            if check_if_html_is_valid_to_get_media_links(res.headers['content-type']):
                # Extract links of the episodes
                content_links = get_links_of_html(str(res.content)) 
                # add the episode links to the result
                for content in content_links:
                    scrapping_result[serie_name][temp_name].append(f"{res.url}{content}")
        except Exception as e:
            continue  
    
    return scrapping_result              
    
                
def get_one_temp(URL_TEMP, verify = True):
    """
    Get the links of one season and save them to a file.

    Args:
        URL_TEMP (str): The URL of the season.
        CARPETA_DESTINO (str): The destination folder path to save the links.
    """
    if not str(URL_TEMP).endswith("/"):
        URL_TEMP += "/"
    
    temp_name = format_key_name(str(URL_TEMP).split('/')[-2])
    scrapping_result = {temp_name: []}
    
    html_temp = requests.get(URL_TEMP, verify=verify).content 
    content_links = get_links_of_html(str(html_temp)) 
    # add the episode links to the result
    for content in content_links:
        scrapping_result[temp_name].append(f"{URL_TEMP}/{content}")
    
    return scrapping_result    
