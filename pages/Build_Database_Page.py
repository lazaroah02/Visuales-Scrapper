import json
import threading
from tkinter import Entry, Button, Label, Text, messagebox, filedialog, ttk, END
from functionalities.build_database import build_database
from requests import RequestException

class BuildDatabasePage(ttk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.root = root

        # Label for input URL of the visuals folder
        self.label_url_carpeta_visuales = Label(self, text="URL carpeta en visuales")
        self.label_url_carpeta_visuales.place(x=10, y=20)

        # Input for the folder URL
        self.input_url_carpeta_visuales = Entry(self)
        self.input_url_carpeta_visuales.config(width=79)
        self.input_url_carpeta_visuales.place(x=10, y=50)

        # Label for database name
        self.label_nombre_db = Label(self, text="Nombre de Base de datos a generar")
        self.label_nombre_db.place(x=10, y=90)

        # Input for the database name
        self.input_nombre_db = Entry(self)
        self.input_nombre_db.config(width=79)
        self.input_nombre_db.place(x=10, y=120)
        
        # Label for destination folder
        self.label_ruta_destino = Label(self, text="Ruta de destino")
        self.label_ruta_destino.place(x=10, y=170)

        # Input for the destination folder path
        self.input_ruta_destino = Entry(self)
        self.input_ruta_destino.config(width=65)
        self.input_ruta_destino.place(x=10, y=200)

        # Button to select the destination folder path
        self.button_select_ruta = Button(self, text="Seleccionar", command=self.seleccionar_ruta_destino)
        self.button_select_ruta.place(x=420, y=195)

        # Button to start generating the database
        self.button = Button(self, text="Generar Base de Datos", command=self.start_generating_database)
        self.button.config()
        self.button.place(x=10, y=240)

        # Label to show the loading status
        self.label_loading = Label(self, text="Generando Base de Datos")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width=20)

        self.x_coordenate_of_loading_points = 375
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
        
        #show log textarea
        self.text_area_log = Text(self)
        self.text_area_log.config(width = 60, height = 11)
        self.text_area_log.place(x = 8, y = 280)
                                        
    def seleccionar_ruta_destino(self):
        """Open a dialog to select the destination folder and update the input field."""
        self.input_ruta_destino.delete(0, "end")
        path = str(filedialog.askdirectory())
        self.input_ruta_destino.insert(0, path)
        
    def start_generating_database(self):
        """Start the process of generating the database in a new thread."""
        url_carpeta_visuales = self.input_url_carpeta_visuales.get()
        ruta_destino = self.input_ruta_destino.get()
        nombre_db = self.input_nombre_db.get()
        
        # Check that no field is empty
        if url_carpeta_visuales == "" or ruta_destino == "" or nombre_db == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        elif "." in nombre_db:
            messagebox.showinfo("!","Nombre para la base de datos no válido")
        else:
            # Start the database generation in a new thread
            t = threading.Thread(target=self.generate_database, args=[url_carpeta_visuales, ruta_destino, nombre_db])
            t.start()   
    
    def generate_database(self, url_carpeta_visuales, ruta_destino, nombre_db):
        """Generate the database and save it to the specified path."""
        self.disable_buttons()
        self.show_loading_status()
        try:
            data = build_database(url_carpeta_visuales, self.log_callback_function)
            with open(f"{ruta_destino}/{nombre_db}.json", "w") as file:
                json.dump(data, file) 
            if data != {}:
                messagebox.showinfo("!","Operacion finalizada con éxito")
            else:
                messagebox.showinfo(
                    "!", 
                    "Se genero una base de datos vacía. Si estas segur@ de que la carpeta tiene contenido revisa el link"
                )   
                self.button.config(text="Reintentar")
       
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text="Reintentar")
        except Exception:
            messagebox.showinfo("!", "Herror al construir la base de datos")   
            self.button.config(text="Reintentar")
        finally:
            self.enable_buttons()
            self.hide_loading_status()      
              
    def enable_buttons(self):
        """Enable the buttons in the UI."""
        self.button.config(state="normal")
        self.button_select_ruta.config(state="normal")
        
    def disable_buttons(self):
        """Disable the buttons in the UI."""
        self.button.config(state="disabled")
        self.button_select_ruta.config(state="disabled")
    
    def show_loading_status(self, frame=0):
        """Show the loading status with an animated effect."""
        if self.loading_points.winfo_x() >= 390:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=150, y=235)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=240)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.root.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        """Hide the loading status."""
        self.root.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()
    
    def log_callback_function(self, log):
        '''function to show a log in the log textarea'''
        self.text_area_log.insert(END, f"•{log}\n \n")
        self.text_area_log.see("end")    
