import time
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from utils.constants import ALLOWED_FORMATS, FILE_EXTENSIONS
from utils.utils import format_key_name

def scrape_visual_folders_recursively(parent_folder_url, log_calback_function,  check_if_stop, verify = True):
    """
    Build a database by recursively scraping links from a parent folder URL.

    Args:
        parent_folder_url (str): The URL of the parent folder to scrape.

    Returns:
        dict or list: A dictionary of links if the folder contains subfolders,
                      or a list of media links if the folder contains media files.
    """
    #check if the program stoped and stop the thread
    if check_if_stop():
        return 
    
    # Delay to avoid overloading the server
    time.sleep(5)
    
    # Ensure the URL ends with a slash
    if not parent_folder_url.endswith("/"):
        parent_folder_url += "/"
    
    log_calback_function(f"Scrapping: {parent_folder_url}")    

    try:
        # Fetch the HTML content of the parent folder URL
        res = requests.get(parent_folder_url, verify=verify)
        
        # Get media links from the HTML content
        media_links = get_media_links_of_html(str(res.content))
        
        # Get folder links from the HTML content
        folders_links = get_folder_links_of_html(str(res.content))

        # Use ThreadPoolExecutor to scrape folders concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_link = {
                executor.submit(
                    scrape_visual_folders_recursively, 
                    parent_folder_url + link, 
                    log_calback_function, 
                    check_if_stop,
                    verify): 
                        format_key_name(link) for link in folders_links
                }
            results = {future_to_link[future]: future.result() for future in concurrent.futures.as_completed(future_to_link)}
        
        # add losed links to the resultant dict
        if len(media_links) > 0 and len(folders_links) > 0:
            key_name = f"{format_key_name(str(parent_folder_url).split('/')[-2])}-links-sueltos"
            results[key_name] = [parent_folder_url + link for link in media_links]
        # if there are only media links return them as a list
        if len(media_links) > 0 and len(folders_links) == 0:
            return [parent_folder_url + link for link in media_links]

        return results
    except Exception as e:
        log_calback_function(f"Error scrapping: {parent_folder_url} || {e}")
        return "Error Getting this folder info"

def get_folder_links_of_html(html):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, features="lxml")
    tags = soup("a")
    folders_links = []
    
    # Extract links from the HTML content, excluding media files
    for tag in tags[5:len(tags)]:
        link = tag.get('href')
        if link == "?C=M&O=D" or link == "../" or link == 'http://emby.uclv.cu':
            continue
        if link and not any(link.endswith(ext) or link.endswith(ext.upper()) for ext in FILE_EXTENSIONS):
            folders_links.append(link)

    return folders_links        

def get_media_links_of_html(html):
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
        if link == "?C=M&O=D" or link == "../" or link == 'http://emby.uclv.cu':
            continue
        if any(link.endswith(ext) or link.endswith(ext.upper()) for ext in ALLOWED_FORMATS):
            if str(link).find("\\") != -1:
                link = str(link).replace("\\","")
            links.append(link)
    return links     