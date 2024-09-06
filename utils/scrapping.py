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
