import time
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from functionalities.scrapping import get_links_of_html
from utils.constants import FILE_EXTENSIONS
from utils.utils import format_key_name

def build_database(parent_folder_url, log_calback_function):
    """
    Build a database by recursively scraping links from a parent folder URL.

    Args:
        parent_folder_url (str): The URL of the parent folder to scrape.

    Returns:
        dict or list: A dictionary of links if the folder contains subfolders,
                      or a list of media links if the folder contains media files.
    """
    # Delay to avoid overloading the server
    time.sleep(5)
    
    # Ensure the URL ends with a slash
    if not parent_folder_url.endswith("/"):
        parent_folder_url += "/"
    
    log_calback_function(f"Scrapping: {parent_folder_url}")    

    try:
        # Fetch the HTML content of the parent folder URL
        res = requests.get(parent_folder_url, verify=False)
        
        # Get media links from the HTML content
        media_links = get_links_of_html(str(res.content))
        if media_links:
            return [parent_folder_url + link for link in media_links]

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(res.content, features="lxml")
        tags = soup("a")
        links = []
        
        # Extract links from the HTML content, excluding media files
        for tag in tags[5:len(tags)]:
            link = tag.get('href')
            if link and not any(link.endswith(ext) or link.endswith(ext.upper()) for ext in FILE_EXTENSIONS):
                links.append(link)

        # Use ThreadPoolExecutor to scrape links concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_link = {
                executor.submit(
                    build_database, 
                    parent_folder_url + link, 
                    log_calback_function): 
                        format_key_name(link) for link in links
                }
            results = {future_to_link[future]: future.result() for future in concurrent.futures.as_completed(future_to_link)}

        return results
    except Exception as e:
        log_calback_function(f"Error scrapping: {parent_folder_url} || {e}")
        return "Error Getting this folder info"