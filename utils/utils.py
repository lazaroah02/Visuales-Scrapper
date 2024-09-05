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

def recovery_idm_path():
    with open("./idm_path.txt", "r") as idm_path_file:
        # Read the first line and delete the blank spaces
        idm_path = idm_path_file.readline().strip()  
        print(idm_path)
        return idm_path      

def update_idm_path(new_path):
    with open("./idm_path.txt", "w") as idm_path_file:
        idm_path_file.write(new_path + "\n")

                      
              