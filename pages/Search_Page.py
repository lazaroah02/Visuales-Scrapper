import json
import threading
from tkinter import Entry, Button, Label, Text
from tkinter import messagebox, filedialog
from tkinter import ttk
from functionalities.search import find_all_matches_in_dict
from requests import RequestException

class SearchPage(ttk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.root = root

        # Label for input load database
        self.label_database_path = Label(self, text="Ruta Base de Datos")
        self.label_database_path.place(x=10, y=20)

        # Input for data base name
        self.input_database_path = Entry(self)
        self.input_database_path.config(width=65)
        self.input_database_path.place(x=10, y=50)
        
        # Button to load data base
        self.button_load_database = Button(self, text="Seleccionar", command=self.load_database)
        self.button_load_database.place(x=420, y=45)

        # Label search value
        self.label_search_value = Label(self, text="Valor a buscar")
        self.label_search_value.place(x=10, y=90)

        # Input for search value
        self.input_search_value = Entry(self)
        self.input_search_value.config(width=79)
        self.input_search_value.place(x=10, y=120)

        # Button to start generating the database
        self.button_search = Button(self, text="Buscar", command=self.start_searching)
        self.button_search.config()
        self.button_search.config()
        self.button_search.place(x=10, y=165)

        # Label to show the loading status
        self.label_loading = Label(self, text="Buscando")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width = 10)

        self.x_coordenate_of_loading_points = 170
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
        
        #text to show the searching result
        self.textarea_search_result = Text(self)
        self.textarea_search_result.config(width = 72, height = 14)
        self.textarea_search_result.place(x = 10, y = 200)
                                        
    def load_database(self):
        """Open a dialog to select the destination folder and update the input field."""
        self.input_database_path.config(state = "normal")
        self.input_database_path.delete(0, "end")
        path = str(filedialog.askopenfilename(parent = self.root, title='Seleccionar base de datos .json', filetypes=[("Json File","*.json")]))
        self.input_database_path.insert(0, path)
        self.input_database_path.config(state = "disabled")
        
    def start_searching(self):
        """Start the process of generating the database in a new thread."""
        search_value = self.input_search_value.get()
        database_path = self.input_database_path.get()
        
        # Check that no field is empty
        if database_path == "" or search_value == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        else:
            # Start the searching
            t = threading.Thread(target=self.search, args=[search_value, database_path])
            t.start()   
    
    def search(self, search_value, database_path):
        """Search in the database the given value"""
        self.disable_buttons()
        self.show_loading_status()
        with open(database_path, "r") as file:
            database_data = json.load(file) 
        try:
            result = find_all_matches_in_dict(database_data, search_value) 
            if result != {}:
                messagebox.showinfo("!","Operacion finalizada con éxito")
            else:
                messagebox.showinfo("!", "No se encontraron coincidencias")   
       
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
        except Exception:
            messagebox.showinfo("!", "Herror al construir la base de datos")   
        finally:
            self.enable_buttons()
            self.hide_loading_status()      
              
    def enable_buttons(self):
        """Enable the buttons in the UI."""
        self.button_search.config(state="normal")
        self.button_load_database.config(state="normal")
        
    def disable_buttons(self):
        """Disable the buttons in the UI."""
        self.button_search.config(state="disabled")
        self.button_load_database.config(state="disabled")
    
    def show_loading_status(self, frame=0):
        """Show the loading status with an animated effect."""
        if self.loading_points.winfo_x() >= 200:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=70, y=163)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=168)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.root.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        """Hide the loading status."""
        self.root.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()
