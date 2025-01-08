import json
import threading
from tkinter import Entry, Button, Label, messagebox, filedialog, ttk, END, Checkbutton, IntVar
from tkinter.scrolledtext import ScrolledText
from functionalities.scrapping import scrape_visual_folders_recursively
from utils.toast import Toast

class BuildDatabasePage(ttk.Frame):
    def __init__(self, parent, check_if_program_stoped, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.check_if_program_stoped = check_if_program_stoped
        
        #variable to store if use https verification or not
        self.use_https_verification = IntVar(value=1)

        #variable to control when to stop the building
        self.stop_building = False

        # Label for input URL of the visuals folder
        self.label_url_carpeta_visuales = Label(self, text="URL carpeta en visuales")
        self.label_url_carpeta_visuales.place(x=10, y=20)

        # Input for the folder URL
        self.input_url_carpeta_visuales = Entry(self)
        self.input_url_carpeta_visuales.config(width=79)
        self.input_url_carpeta_visuales.place(x=10, y=50)
        
        #checkbox check https certificate
        self.checkbox_use_https_verification = Checkbutton(self, variable=self.use_https_verification, text="Usar verificación https", onvalue=1, offvalue=0)
        self.checkbox_use_https_verification.place(x=5, y=70)

        # Label for database name
        self.label_nombre_db = Label(self, text="Nombre de Base de datos a generar")
        self.label_nombre_db.place(x=10, y=100)

        # Input for the database name
        self.input_nombre_db = Entry(self)
        self.input_nombre_db.config(width=79)
        self.input_nombre_db.place(x=10, y=130)
        
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
        self.text_area_log = ScrolledText(self, width = 58, height = 10)
        self.text_area_log.place(x = 8, y = 280)
        
        # Button to stop the building
        self.button_stop_building = Button(self, text="Detener", command = self.handle_stop_building)
        self.button_stop_building.config()
        self.button_stop_building.place(x=10, y=447)
        
        self.bind('<Return>', self.start_generating_database)
        self.input_ruta_destino.bind('<Return>', self.start_generating_database)
                                                
    def seleccionar_ruta_destino(self):
        """Open a dialog to select the destination folder and update the input field."""
        self.input_ruta_destino.delete(0, "end")
        path = str(filedialog.askdirectory(initialdir = "D:\\Projects\\Visuales Scrapper\\databases"))
        self.input_ruta_destino.insert(0, path)
        
    def start_generating_database(self, event = None):
        """Start the process of generating the database in a new thread."""
        url_carpeta_visuales = self.input_url_carpeta_visuales.get()
        ruta_destino = self.input_ruta_destino.get()
        nombre_db = self.input_nombre_db.get()
        self.stop_building = False
        
        # Check that no field is empty
        if url_carpeta_visuales == "" or ruta_destino == "" or nombre_db == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        elif "." in nombre_db:
            messagebox.showinfo("!","Nombre para la base de datos no válido")
        else:
            # Start the database generation in a new thread
            self.disable_buttons()
            self.show_loading_status()
            t = threading.Thread(target=self.generate_database, args=[url_carpeta_visuales, ruta_destino, nombre_db])
            t.daemon = True
            t.start()   
    
    def generate_database(self, url_carpeta_visuales, ruta_destino, nombre_db):
        """Generate the database and save it to the specified path."""
        try:
            data = scrape_visual_folders_recursively(
                url_carpeta_visuales, 
                self.log_callback_function, 
                self.check_if_stop,
                verify = self.use_https_verification.get() == 1
                )
            #if the program was stoped, don't show any message
            if self.check_if_stop():
                return
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
        except Exception as e:
            messagebox.showinfo("!", "Herror al construir la base de datos") 
            self.log_callback_function(f"Herror al construir la base de datos: {e}")  
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
        #if the program stoped, don't show loading status
        if self.check_if_program_stoped():
            return
        if self.loading_points.winfo_x() >= 390:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=150, y=235)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=240)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        """Hide the loading status."""
        #if the program stoped, don't show loading status
        if self.check_if_program_stoped():
            return
        self.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()
    
    def log_callback_function(self, log):
        '''function to show a log in the log textarea'''
        self.text_area_log.insert(END, f"•{log}\n \n")
        self.text_area_log.see("end")    
    
    def check_if_stop(self):
        """FUnction to check if the building must stop"""
        return self.stop_building or self.check_if_program_stoped() 
    
    def handle_stop_building(self):
        """Function to stop the building process"""
        if self.stop_building == True:
            return messagebox.showinfo("!", "No hay nada que detener")
        self.stop_building = True  
        Toast(self.parent, title = "Stoping", message = "La operacion se detendra en breve ...")
        self.hide_loading_status()
        self.enable_buttons()
