import os
from urllib.parse import unquote

def center_window(ancho,alto,raiz):
    x_ventana = raiz.winfo_screenwidth() // 2 - ancho // 2
    y_ventana = raiz.winfo_screenheight() // 2 - alto // 2

    posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
    return posicion

def check_if_html_is_valid_to_get_media_links(header):
    return header == 'text/html;charset=UTF-8' or header == 'text/html;charset=utf-8' or header == 'text/html; charset=UTF-8' or header == 'text/html; charset=utf-8'

def format_key_name(key):
    return unquote(key.replace("/",""))

def clean_folder(folder):
    #remove all files from a folder
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def folder_exists(path):
    try:
        os.listdir(path)
        return True
    except:
        return False 

def file_exists(path):
    try:
        if os.path.exists(path):
            return True
        else:
            return False
    except:
        return False          

def recovery_idm_path():
    try:
        #check if the txt file exists
        if file_exists("./idm_path.txt"):
            with open("./idm_path.txt", "r") as idm_path_file:
                # Read the first line and delete the blank spaces
                idm_path = idm_path_file.readline().strip()  
                return idm_path   
        else:
            #create txt file with the idm path
            update_idm_path("C:/Program Files (x86)/Internet Download Manager/IDMan.exe")   
            return "C:/Program Files (x86)/Internet Download Manager/IDMan.exe"
    except:
        return ""      

def update_idm_path(new_path):
    with open("./idm_path.txt", "w") as idm_path_file:
        idm_path_file.write(new_path + "\n")
        
def validate_folder_name(folder_name):
    '''Check that folder_name does not start or end with dot and create the folder if valid'''
    folder_name = str(folder_name)
    
    # Remove leading and trailing dots
    if folder_name.startswith("."):
        folder_name = folder_name[1:]
    if folder_name.endswith("."):
        folder_name = folder_name[:-1]
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        folder_name = folder_name.replace(char, "")   

    return folder_name
      

                      
              