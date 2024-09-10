import json
import os
import subprocess
import threading
from tkinter import Entry, Button, Frame, Label, Checkbutton, IntVar, ttk, messagebox, filedialog, END
from components.collapsible_pane import CollapsiblePane
from functionalities.search import find_all_matches_in_dict
from utils.utils import clean_folder, recovery_idm_path, update_idm_path, validate_folder_name
from utils.constants import DATABASE_DIRECTORY
from components.scrollable_frame import ScrollableFrame

class SearchPage(ttk.Frame):
    def __init__(self, parent, check_if_program_stoped, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.check_if_program_stoped = check_if_program_stoped
        
        #variable to save the search results
        self.search_results = {}
        
        #variable to save if the user wants to remember the database or not
        self.remember_database = IntVar(value=1)

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
        
        #checkbox remember database
        self.checkbox_remember_database = Checkbutton(self, variable=self.remember_database, text="Recordar Base de Datos", onvalue=1, offvalue=0)
        self.checkbox_remember_database.place(x=5, y=70)
        
        # Label search value
        self.label_search_value = Label(self, text="Valor a buscar")
        self.label_search_value.place(x=10, y=100)

        # Input for search value
        self.input_search_value = Entry(self)
        self.input_search_value.config(width=79)
        self.input_search_value.place(x=10, y=130)

        # Button to start generating the database
        self.button_search = Button(self, text="Buscar", command=self.start_searching)
        self.button_search.place(x=10, y=165)

        # Label to show the loading status
        self.label_loading = Label(self, text="Buscando")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width = 10)

        self.x_coordenate_of_loading_points = 180
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
        
        #container of the show searching result component
        self.show_search_results_container = Frame(self, width=58, height=14, borderwidth=1, relief="solid")
        self.show_search_results_container.place(x=10, y=200)
        
        #show searching result component
        self.searching_results_ui_representation_elements = []
        self.show_search_results_box = ScrollableFrame(self.show_search_results_container)
        self.show_search_results_box.pack(fill="both", expand=False)
        
        # Button to export searching results as files
        self.button_export_searching_results_as_files = Button(self, text="Exportar como archivos", command=self.start_exporting_as_files)
        self.button_export_searching_results_as_files.place(x=120, y=440)
        
        # Button to export searching results to idm
        self.button_export_searching_results_to_idm = Button(self, text="Exportar a IDM", command=self.start_exporting_to_idm)
        self.button_export_searching_results_to_idm.place(x=10, y=440)
        
        self.recovery_remembered_database()
        self.bind('<Return>', self.start_searching)
        self.input_search_value.bind('<Return>', self.start_searching)
                                                
    def load_database(self):
        """Open a dialog to select the database"""
        self.input_database_path.config(state = "normal")
        self.input_database_path.delete(0, "end")
        path = str(
            filedialog.askopenfilename(
                parent = self, 
                title='Seleccionar base de datos .json', 
                filetypes=[("Json File","*.json")],
                initialdir = "D:\\Projects\\Visuales Scrapper\\databases"
                ))
        self.input_database_path.insert(0, path)
        self.input_database_path.config(state = "disabled")
        
    def start_searching(self, event = None):
        """Start the process of searching in the database"""
        search_value = self.input_search_value.get()
        database_path = self.input_database_path.get()
        
        # Check that no field is empty
        if database_path == "" or search_value == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        else:   
            #check if remember database or not
            if self.remember_database.get() == 1:
                self.handle_remember_database() 
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
            results = find_all_matches_in_dict(database_data, search_value) 
            self.search_results = results
            if results == {}:
                messagebox.showinfo("!", "No se encontraron coincidencias")       
            else:
                self.show_searching_result(results)
                messagebox.showinfo("!","Operacion finalizada con éxito")
         
        except Exception as e:
            messagebox.showinfo("!", "Herror al realizar la busqueda: " + str(e))   
        finally:
            self.enable_buttons()
            self.hide_loading_status()      
              
    def enable_buttons(self):
        """Enable the buttons in the UI."""
        self.button_search.config(state="normal")
        self.button_load_database.config(state="normal")
        self.button_export_searching_results_as_files.config(state="normal")
        self.button_export_searching_results_to_idm.config(state="normal")
        
    def disable_buttons(self):
        """Disable the buttons in the UI."""
        self.button_search.config(state="disabled")
        self.button_load_database.config(state="disabled")
        self.button_export_searching_results_as_files.config(state="disabled")
        self.button_export_searching_results_to_idm.config(state="disabled")
    
    def show_loading_status(self, frame=0):
        """Show the loading status with an animated effect."""
        #if the program stoped, don't show loading status
        if self.check_if_program_stoped():
            return
        if self.loading_points.winfo_x() >= 200:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=70, y=163)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=168)
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

    def handle_remember_database(self):
        #recovery database info
        database_path = self.input_database_path.get()
        database_name = database_path.split("/")[-1]
        #read database data
        with open(database_path, "r") as file:
            database_data = json.load(file)
        #remove old database
        clean_folder(DATABASE_DIRECTORY)    
        #save database copy    
        with open(f"{DATABASE_DIRECTORY}/{database_name}", "w") as f:
            json.dump(database_data, f)     
    
    def recovery_remembered_database(self):
        try:
            for file in os.listdir(DATABASE_DIRECTORY):
                if file.endswith('.json'):
                    ruta_bd = DATABASE_DIRECTORY + "/" + file
                    self.input_database_path.config(state = "normal")
                    self.input_database_path.delete(0, "end")
                    self.input_database_path.insert(0, ruta_bd)
                    self.input_database_path.config(state = "disabled")
        except:
            pass            
    
    def show_searching_result(self, results):
        """
        Show the searching results on the log textarea for user to visualize if the output is correct.

        Args:
            results (dict): A dictionary where the keys are show names and the values are seasons or links.
        
        Note: results Structure: results is a dict that may have other dicts inside,
            that's why the validation of the structure to iterate if it is a list or a dict.
            Example:
            {
                "Iron Man": ["link_movie", "link_subtitle"],
                "Aida": {
                    "temp1": ["cap1_link", "cap2_link"],
                    "temp2": ["cap1_link", "cap2_link"],
                }
            }
        """
        # delete all the previous showed elements
        for element in self.searching_results_ui_representation_elements:
            element.destroy()
        
        for show, seasons in results.items(): 
            show_collapsable = CollapsiblePane(
                self.show_search_results_box.scrollable_frame, 
                self.show_search_results_box.update_scrollregion, 
                title = str(show)
                )
            show_collapsable.pack(fill="x", pady=5, padx=5)
            self.searching_results_ui_representation_elements.append(show_collapsable)
            if isinstance(seasons, dict):
                for season, links in seasons.items():
                    season_collapsable = CollapsiblePane(
                        show_collapsable, 
                        self.show_search_results_box.update_scrollregion, 
                        title = str(season),
                        elements_text_list=links
                        )
                    season_collapsable.grid(row=1, column=0, sticky="w", padx=10)
                    self.searching_results_ui_representation_elements.append(season_collapsable)
            elif isinstance(seasons, list):
                show_collapsable.elements_text_list = seasons
                show_collapsable.render_element_list()
            else:
                pass       

    def export_searching_results_as_files(self):
        """
        Export the searching results to the desired folder.

        If there are no search results, show an information message.

        Args:
            None
        
        Note: self.search_results Structure: self.search_results is a dict that may have other dicts inside,
            that's why the validation of the structure to iterate if it is a list or a dict.
            Example:
            {
                "Iron Man": ["link_movie", "link_subtitle"],
                "Aida": {
                    "temp1": ["cap1_link", "cap2_link"],
                    "temp2": ["cap1_link", "cap2_link"],
                }
            }
        """
        """
        url = "http://localhost:8080/Aida/01/Aida%20-%201x01%20-%20Una%20Vida%20Nueva%20.avi" 
        download_path = "D:/"  # Carpeta de destino
        idm_path = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"
        subprocess.run([idm_path, '/d', url, '/p', download_path, '/n', '/a'])
        """
        try:
            if not self.search_results:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            if not carpeta_destino:
                return
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            for show, seasons in self.search_results.items():
                #if the program stoped, stop the exportation
                if self.check_if_stop():
                    return
                carpeta_programa = os.path.join(carpeta_destino, validate_folder_name(show))
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descargar visuales)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                if isinstance(seasons, dict):
                    for season, links in seasons.items():
                        carpeta_temporada = os.path.join(carpeta_programa, validate_folder_name(season))
                        os.makedirs(carpeta_temporada, exist_ok=True)
                        with open(f"{carpeta_temporada}/enlaces.txt", "w", encoding="utf-8") as file:
                            for link in links:
                                file.write(f"{link}\n")
                elif isinstance(seasons, list):
                    with open(f"{carpeta_programa}/enlaces.txt", "w", encoding="utf-8") as file:
                        for link in seasons:
                            file.write(f"{link}\n")
                else:
                    messagebox.showinfo("!Error", "Error al exportar")             
            
            messagebox.showinfo("!", "Exportación Exitosa")
        except Exception as e:
            messagebox.showinfo("!Error", "Error al exportar")    
        finally:    
            self.label_loading.config(text="Buscando")
            self.hide_loading_status()
            self.enable_buttons()

    def export_searching_results_to_idm(self):
        """
        Export the searching results to idm for downloading.

        If there are no search results, show an information message.

        Args:
            None
        
        Note: self.search_results Structure: self.search_results is a dict that may have other dicts inside,
            that's why the validation of the structure to iterate if it is a list or a dict.
            Example:
            {
                "Iron Man": ["link_movie", "link_subtitle"],
                "Aida": {
                    "temp1": ["cap1_link", "cap2_link"],
                    "temp2": ["cap1_link", "cap2_link"],
                }
            }
        """
        try:
            idm_path = recovery_idm_path()
            
            # check if IDM is correctly installed and exists in the provided folder. Otherwise ask user for the new IDM location
            if not os.path.isfile(idm_path):
                choice = messagebox.askyesno(
                    "IDM no encontrado", 
                    "IDM no está instalado o la ruta de IDM indicada no es correcta. ¿Quieres seleccionar una nueva ruta?"
                    )
                if not choice:
                    return
                
                new_idm_path = filedialog.askopenfilename(title="Selecciona IDMan.exe", filetypes=[("IDMan.exe", "IDMan.exe")])
                if new_idm_path and os.path.isfile(new_idm_path):
                    messagebox.showinfo("!", "Ruta de IDM actualizada correctamente. Continuaremos con la exportación.")
                    idm_path = new_idm_path
                    update_idm_path(new_idm_path)
                else:
                    return messagebox.showinfo("Error", "No se seleccionó una ruta válida para IDM. Pruebe exportar como archivo")    
            
            if not self.search_results:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            if not carpeta_destino:
                return
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            for show, seasons in self.search_results.items():
                #if the program stoped, stop the exportation
                if self.check_if_stop():
                    return   
                
                carpeta_programa = os.path.join(carpeta_destino, validate_folder_name(show))
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descarga automatica con IDM)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                if isinstance(seasons, dict):
                    for season, links in seasons.items():
                        carpeta_temporada = os.path.join(carpeta_programa, validate_folder_name(season))
                        os.makedirs(carpeta_temporada, exist_ok=True)
                        for link in links:
                            subprocess.run([idm_path, '/d', link, '/p', carpeta_temporada, '/n', '/a'])
                elif isinstance(seasons, list):
                    for link in seasons:
                        subprocess.run([idm_path, '/d', link, '/p', carpeta_programa, '/n', '/a'])
                else:
                    messagebox.showinfo("!Error", "Error al exportar")           
            
            messagebox.showinfo("!", "Exportación Exitosa")
        except Exception as e:
            messagebox.showinfo("!Error", "Error al exportar")    
        finally:    
            self.label_loading.config(text="Buscando")
            self.hide_loading_status()
            self.enable_buttons()
    
    def start_exporting_to_idm(self):
        threading.Thread(target=self.export_searching_results_to_idm).start()
    
    def start_exporting_as_files(self):    
        threading.Thread(target=self.export_searching_results_as_files).start()
    
    def check_if_stop(self):
        """Function to check if the user closed or stoped the program"""
        return self.check_if_program_stoped()       