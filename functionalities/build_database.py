import time
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from utils.scrapping import get_links_of_html
from utils.constants import FILE_EXTENSIONS
from utils.utils import format_key_name

def build_database(parent_folder_url, log_calback_function,  check_if_stop, verify = True):
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
        media_links = get_links_of_html(str(res.content))

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(res.content, features="lxml")
        tags = soup("a")
        folders_links = []
        
        # Extract links from the HTML content, excluding media files
        for tag in tags[5:len(tags)]:
            link = tag.get('href')
            if link and not any(link.endswith(ext) or link.endswith(ext.upper()) for ext in FILE_EXTENSIONS):
                folders_links.append(link)

        # Use ThreadPoolExecutor to scrape folders concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_link = {
                executor.submit(
                    build_database, 
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