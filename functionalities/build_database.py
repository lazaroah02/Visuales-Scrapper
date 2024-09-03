import time
from bs4 import BeautifulSoup
import requests
import json
import concurrent.futures
from functionalities.scrapping import get_links_of_html
from utils.constants import FILE_EXTENSIONS
from utils.utils import format_key_name

def build_database(parent_folder_url):
    time.sleep(5)
    if not parent_folder_url.endswith("/"):
        parent_folder_url += "/"

    try:
        res = requests.get(parent_folder_url)
        media_links = get_links_of_html(str(res.content))
        if media_links:
            return [parent_folder_url + link for link in media_links]

        soup = BeautifulSoup(res.content, features="lxml")
        tags = soup("a")
        links = []
        for tag in tags[5:len(tags)]:
            link = tag.get('href')
            if link and not any(link.endswith(ext) or link.endswith(ext.upper()) for ext in FILE_EXTENSIONS):
                links.append(link)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_link = {executor.submit(build_database, parent_folder_url + link): format_key_name(link) for link in links}
            results = {future_to_link[future]: future.result() for future in concurrent.futures.as_completed(future_to_link)}

        return results
    except requests.exceptions.RequestException as e:
        print("There was an error processing the request: " + str(e)) 
    except Exception as e:
        print("There was an error: " + str(e))      

data = build_database("http://192.168.137.104:8000/")
with open("./my_file.json", "w") as file:
    json.dump(data, file)    
