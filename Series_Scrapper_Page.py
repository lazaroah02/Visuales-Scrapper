import threading
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import scrapping
from requests import RequestException

class Series_Scrapper_Page(ttk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.root = root

        # Label del input url_serie
        self.label_url_serie = Label(self, text="URL de la serie")
        self.label_url_serie.place(x=10, y=10)

        # Input para la url de la serie
        self.input_url_serie = Entry(self)
        self.input_url_serie.config(width=50)
        self.input_url_serie.place(x=100, y=10)

        # Label carpeta de destino
        self.label_ruta_destino = Label(self, text="Ruta de destino")
        self.label_ruta_destino.place(x=10, y=80)

        # Input para la ruta de la carpeta de destino
        self.input_ruta_destino = Entry(self)
        self.input_ruta_destino.config(width=50)
        self.input_ruta_destino.place(x=100, y=80)

        # Botón para seleccionar la ruta de la carpeta de destino
        self.button_select_ruta = Button(self, text="Seleccionar", command=self.seleccionar_ruta_destino)
        self.button_select_ruta.place(x=420, y=75)

        self.type_of_scrapping = {
            "none": "Tipo de Scrapping",
            "serie": "Serie Completa",
            "temp": "Temporada",
        }

        # Combobox para seleccionar si lo que se va a descargar es una serie completa o temporada
        self.box_serie_or_temp = ttk.Combobox(self, text="Tipo de Scrapping", state="readonly",
                                              values=[self.type_of_scrapping["serie"], self.type_of_scrapping["temp"]])
        self.box_serie_or_temp.set(self.type_of_scrapping["none"])
        self.box_serie_or_temp.config(width=30)
        self.box_serie_or_temp.place(x=15, y=150)

        # Botón para iniciar el scrapping para una serie
        self.button = Button(self, text="Iniciar Scrapping", command=self.iniciar_scrapping)
        self.button.config()
        self.button.place(x=230, y=148)

        # Label to show the loading status
        self.label_loading = Label(self, text="Cargando")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width=10)

        self.x_coordenate_of_loading_points = 240
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
                        
    def seleccionar_ruta_destino(self):
        self.input_ruta_destino.delete(0, "end")
        path = str(filedialog.askdirectory())
        self.input_ruta_destino.insert(0, path)
        
    def iniciar_scrapping(self):
        url_serie = self.input_url_serie.get()
        ruta_destino = self.input_ruta_destino.get()
        type_of_scrapping = self.box_serie_or_temp.get()
        
        #check that any field is empty
        if url_serie == "" or ruta_destino == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        elif type_of_scrapping == self.type_of_scrapping["none"]:    
            messagebox.showinfo("!","Selecciona un tipo de Scrapping")
        else:
            #if the user want to download a full serie
            if type_of_scrapping == self.type_of_scrapping["serie"]:
                t = threading.Thread(target = self.scrapping_serie, args = [url_serie, ruta_destino])
                t.start()   
            #if the user want to download only one temp
            else:
                t = threading.Thread(target = self.scrapping_one_temp, args = [url_serie, ruta_destino])
                t.start() 
    
    #get the links of one full serie, including all temps        
    def scrapping_serie(self, url_serie, ruta_destino):
        self.disable_buttons()
        self.show_loading_status()
        try:
            scrapping.scrapping(url_serie, ruta_destino)
            messagebox.showinfo("!","Operacion finalizada con éxito")
            self.enable_buttons()
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text = "Reintentar")
            self.enable_buttons()
        except Exception:
            messagebox.showinfo("!", "Herror al obtener los links")   
            self.button.config(text = "Reintentar")
            self.enable_buttons()  
        finally:
            self.hide_loading_status()      
    
    #get the links of one temp of the serie  
    def scrapping_one_temp(self, url_serie, ruta_destino):
        self.disable_buttons()
        self.show_loading_status()
        try:
            scrapping.get_one_temp(url_serie, ruta_destino)
            messagebox.showinfo("!","Operacion finalizada con éxito")
            self.enable_buttons()            
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text = "Reintentar")
            self.enable_buttons()
        except Exception:
            messagebox.showinfo("!", "Herror al obtener los links")   
            self.button.config(text = "Reintentar")
            self.enable_buttons() 
        finally:
            self.hide_loading_status()  
              
    def enable_buttons(self):
        self.button.config(state = "normal")
        self.button_select_ruta.config(state = "normal")
        
    def disable_buttons(self):
        self.button.config(state = "disabled")
        self.button_select_ruta.config(state = "disabled")
    
    # Define a function to animate the GIF
    def show_loading_status(self, frame = 0):
        if self.loading_points.winfo_x() >= 270:
            self.loading_points.place(x = self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x = 120, y = 200)     
        self.loading_points.place(x = (self.x_coordenate_of_loading_points + frame), y = 200)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.root.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        self.root.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()   
