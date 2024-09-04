import os


def center_window(ancho,alto,raiz):
    x_ventana = raiz.winfo_screenwidth() // 2 - ancho // 2
    y_ventana = raiz.winfo_screenheight() // 2 - alto // 2

    posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
    return posicion

def check_if_html_is_valid_to_get_media_links(header):
    return header == 'text/html;charset=UTF-8' or header == 'text/html;charset=utf-8' or header == 'text/html; charset=UTF-8' or header == 'text/html; charset=utf-8'

def format_key_name(key):
    return key.replace("%20", " ").replace("/", "").replace("%28", "(").replace("%29", ")")

def clean_folder(folder):
    #remove all files from a folder
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)