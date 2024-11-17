import os
import subprocess
import threading
from tkinter import END, Checkbutton, Entry, Button, Frame, Label, IntVar, messagebox, filedialog, ttk
from tkinter.scrolledtext import ScrolledText
from components.collapsible_pane import CollapsiblePane
from components.scrollable_frame import ScrollableFrame
from components.select_all_elements import SelectAllElements
from components.selectable import Selectable
from functionalities.scrapping import scrape_visual_folders_recursively
from requests import RequestException
from utils.utils import format_key_name, validate_folder_name

from utils.utils import recovery_idm_path, update_idm_path

class SpecificMediaScrapperPage(ttk.Frame):
    def __init__(self, parent, check_if_program_stoped, *args, **kwargs):
        """
        Initialize the SpecificMediaScrapperPage with UI elements for scraping series.

        Args:
            parent (tk.Widget): The parent widget.
        """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.check_if_program_stoped = check_if_program_stoped
        
        #variable to store if use https verification or not
        self.use_https_verification = IntVar(value=1)
        
        #variable to save the scrapping results
        self.scrapping_results = {}

        # Label for input URL of the series
        self.label_url_serie = Label(self, text="Folder Media URL")
        self.label_url_serie.place(x=10, y=20)

        # Input for the series URL
        self.input_url_serie = Entry(self)
        self.input_url_serie.config(width=62)
        self.input_url_serie.place(x=110, y=20)
        
        #checkbox check https certificate
        self.checkbox_use_https_verification = Checkbutton(self, variable=self.use_https_verification, text="Usar verificación https", onvalue=1, offvalue=0)
        self.checkbox_use_https_verification.place(x=6, y=50)

        # Button to start scraping for a series
        self.button = Button(self, text="Iniciar Scrapping", command=self.iniciar_scrapping)
        self.button.config()
        self.button.place(x=10, y=100)

        # Label to show the loading status
        self.label_loading = Label(self, text="Procesando")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width = 10)

        self.x_coordenate_of_loading_points = 230
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
        
        #container of the show searching result component
        self.show_search_results_container = Frame(self, width=58, height=20, borderwidth=1, relief="solid")
        self.show_search_results_container.place(x=10, y=150)
        
        #show searching result component
        self.searching_results_ui_representation_elements = []
        self.show_search_results_box = ScrollableFrame(self.show_search_results_container, height=250)
        self.show_search_results_box.pack(fill="both", expand=False)
        
        #select all searching results component
        self.select_all_search_results_to_export = SelectAllElements(self.show_search_results_box.scrollable_frame)
        self.select_all_search_results_to_export.pack(fill="x", pady=5, padx=5)
        
        # Button to export scrapping results as files
        self.button_export_scrapping_results_as_files = Button(self, text="Exportar como archivos", command=self.start_exporting_as_files)
        self.button_export_scrapping_results_as_files.place(x=120, y=440)
        
        # Button to export scrapping results to idm
        self.button_export_scrapping_results_to_idm = Button(self, text="Exportar a IDM", command=self.start_exporting_to_idm)
        self.button_export_scrapping_results_to_idm.place(x=10, y=440)
        
        self.bind('<Return>', self.iniciar_scrapping)
        self.input_url_serie.bind('<Return>', self.iniciar_scrapping)
                
    def iniciar_scrapping(self, event = None):
        """Start the scraping process based on the selected type of scrapping."""
        url_serie = self.input_url_serie.get()
        
        # Check that no field is empty
        if url_serie == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        else:
            t = threading.Thread(target=self.scrapping_serie, args=[url_serie])
            t.start()   
    
    def scrapping_serie(self, url_serie):
        """Get the links of a full series, including all seasons."""
        self.disable_buttons()
        self.show_loading_status()
        
        #creating the key to form the dict with the scrapping results
        if url_serie.endswith("/"): key_name = format_key_name(url_serie.split("/")[-2])
        else: key_name = format_key_name(url_serie.split("/")[-1])
                
        try:
            self.scrapping_results = {f"{key_name}": scrape_visual_folders_recursively(
                url_serie, 
                lambda x: None, 
                self.check_if_stop,
                verify = self.use_https_verification.get() == 1
                )}
            
            #if the program stoped, don't show any message'
            if self.check_if_stop():
                return

            self.show_scrapping_result(self.scrapping_results)
            self.enable_buttons()
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text="Reintentar")
            self.enable_buttons()
        except Exception as e:
            messagebox.showinfo("!", "Herror en el scrapping") 
            self.button.config(text="Reintentar")
            self.enable_buttons()  
        finally:
            self.hide_loading_status()      
              
    def enable_buttons(self):
        """Enable the buttons in the UI."""
        self.button.config(state="normal")
        self.button_export_scrapping_results_as_files.config(state="normal")
        self.button_export_scrapping_results_to_idm.config(state="normal")
        
    def disable_buttons(self):
        """Disable the buttons in the UI."""
        self.button.config(state="disabled")
        self.button_export_scrapping_results_as_files.config(state="disabled")
        self.button_export_scrapping_results_to_idm.config(state="disabled")
    
    def show_loading_status(self, frame=0):
        """Show the loading status with an animated effect."""
        #if the program stoped, don't show loading status
        if self.check_if_program_stoped():
            return
        if self.loading_points.winfo_x() >= 250:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=120, y=98)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=103)
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

    def show_scrapping_result(self, results):
        """
        Show the scrapping results for user to visualize if the output is correct. 
        The way that the scrapping results is showed is through an anidated group of collapsable pane where each one is a folder
        and can have inside subfolders(collapsable panes too) or selectables component for media link.
        The object is that the user can select what content export.

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
        #reset the list that storage ui elements    
        self.searching_results_ui_representation_elements = []  
        self.select_all_search_results_to_export.elements_to_select = []
            
        # iterate over each serie, show or movie and create a collapsible pane for each one
        for show, seasons in results.items(): 
            show_collapsable = CollapsiblePane(
                self.show_search_results_box.scrollable_frame, 
                self.show_search_results_box.update_scrollregion, 
                title = str(show)
            )
            show_collapsable.pack(fill="x", pady=5, padx=5)
            #add the collapsable to the searching results ui elements list for future iteration
            self.searching_results_ui_representation_elements.append(show_collapsable)
            #add the collapsable to the select all results ui elements list for select or deselect all the elements
            self.select_all_search_results_to_export.elements_to_select.append(show_collapsable)
            
            if isinstance(seasons, dict):
                #seasons counter. Start in 2 because the position 1 belongs to 'select all component'
                cont_seasons = 2
                
                #iterate over each season folder and create a collapsible pane for each one
                for season, links in seasons.items():
                    season_collapsable = CollapsiblePane(
                        show_collapsable.content_container, 
                        self.show_search_results_box.update_scrollregion, 
                        title = str(season),
                    )
                    season_collapsable.grid(row=cont_seasons, column=0, sticky="w", padx=10)
                    
                    # add the season_collapsable to the parent children list
                    show_collapsable.add_child(season_collapsable)
                    
                    cont_seasons += 1
                    #links of episodes or media counter. Start in 2 because the position 1 belongs to 'select all component'
                    cont_links = 2 
                    
                    #iterate over each link in the folder and create a selectable component for each one
                    for link in links:
                        link_selectable = Selectable(season_collapsable.content_container, text=link)
                        link_selectable.grid(row=cont_links, column=0, sticky="w", padx=10)
                        # add the selectable to the parent children list
                        season_collapsable.add_child(link_selectable) 
                        cont_links += 1
            
            elif isinstance(seasons, list):
                #links of episodes or media counter. Start in 2 because the position 1 belongs to 'select all component'
                cont_links = 2
                
                #iterate over each link in the folder and create a selectable component for each one
                for link in seasons:
                    link_selectable = Selectable(show_collapsable.content_container, text=link)
                    link_selectable.grid(row=cont_links, column=0, sticky="w", padx=10)
                    # add the selectable to the parent children list
                    show_collapsable.add_child(link_selectable)
                    cont_links += 1
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
        try:
            if not self.searching_results_ui_representation_elements:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            
            if not carpeta_destino:
                return
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            for collapsable in self.searching_results_ui_representation_elements:
                #if the program stoped, stop the exportation
                if self.check_if_stop():
                    return
                
                if collapsable.selected.get() == 0:
                    continue
                
                carpeta_programa = os.path.join(carpeta_destino, validate_folder_name(collapsable.title))
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descargar visuales)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                for child in collapsable.selectable_children:
                    
                    if child.selected.get() == 0:
                        continue
                    
                    if isinstance(child, CollapsiblePane):
                        carpeta_temporada = os.path.join(carpeta_programa, validate_folder_name(child.title))
                        os.makedirs(carpeta_temporada, exist_ok=True)
                        
                        with open(f"{carpeta_temporada}/enlaces.txt", "w", encoding="utf-8") as file:
                            for selectable in child.selectable_children:
                                if selectable.selected.get() == 0:
                                    continue
                                file.write(f"{selectable.text}\n")
                                    
                    elif isinstance(child, Selectable):
                        with open(f"{carpeta_programa}/enlaces.txt", "a", encoding="utf-8") as file:
                            file.write(f"{child.text}\n") 
                                
                    else:
                        pass                       
            
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
            
            if not self.searching_results_ui_representation_elements:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            
            if not carpeta_destino:
                return
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            for collapsable in self.searching_results_ui_representation_elements:
                #if the program stoped, stop the exportation
                if self.check_if_stop():
                    return   
                
                if collapsable.selected.get() == 0:
                    continue
                
                carpeta_programa = os.path.join(carpeta_destino, validate_folder_name(collapsable.title))
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descarga automatica con IDM)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                for child in collapsable.selectable_children: 
                    
                    if child.selected.get() == 0:
                        continue
                    
                    if isinstance(child, CollapsiblePane):
                        carpeta_temporada = os.path.join(carpeta_programa, validate_folder_name(child.title))
                        os.makedirs(carpeta_temporada, exist_ok=True)
                        
                        for selectable in child.selectable_children:
                            if selectable.selected.get() == 0:
                                continue
                            subprocess.run([idm_path, '/d', selectable.text, '/p', carpeta_temporada, '/n', '/a'])
                    
                    elif isinstance(child, Selectable):
                        subprocess.run([idm_path, '/d', child.text, '/p', carpeta_programa, '/n', '/a'])
                    
                    else:
                        pass           
            
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