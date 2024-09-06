import os
import subprocess
import threading
from tkinter import END, Checkbutton, Entry, Button, Label, IntVar, Text, messagebox, filedialog, ttk
import functionalities.scrapping as scrapping
from requests import RequestException

from utils.utils import recovery_idm_path, update_idm_path

class SeriesScrapperPage(ttk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        """
        Initialize the SeriesScrapperPage with UI elements for scraping series.

        Args:
            parent (tk.Widget): The parent widget.
            root (tk.Tk): The root Tkinter window.
        """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.root = root
        
        #variable to store if use https verification or not
        self.use_https_verification = IntVar(value=1)
        
        #variable to save the scrapping results
        self.scrapping_results = {}

        # Label for input URL of the series
        self.label_url_serie = Label(self, text="URL de la serie")
        self.label_url_serie.place(x=10, y=20)

        # Input for the series URL
        self.input_url_serie = Entry(self)
        self.input_url_serie.config(width=63)
        self.input_url_serie.place(x=100, y=20)
        
        #checkbox check https certificate
        self.checkbox_use_https_verification = Checkbutton(self, variable=self.use_https_verification, text="Usar verificación https", onvalue=1, offvalue=0)
        self.checkbox_use_https_verification.place(x=6, y=50)

        self.type_of_scrapping = {
            "none": "Tipo de Scrapping",
            "serie": "Serie Completa",
            "temp": "Temporada",
        }

        # Combobox to select whether to download a full series or a season
        self.box_serie_or_temp = ttk.Combobox(self, text="Tipo de Scrapping", state="readonly",
                                              values=[self.type_of_scrapping["serie"], self.type_of_scrapping["temp"]])
        self.box_serie_or_temp.set(self.type_of_scrapping["none"])
        self.box_serie_or_temp.config(width=75)
        self.box_serie_or_temp.place(x=10, y=100)

        # Button to start scraping for a series
        self.button = Button(self, text="Iniciar Scrapping", command=self.iniciar_scrapping)
        self.button.config()
        self.button.place(x=10, y=148)

        # Label to show the loading status
        self.label_loading = Label(self, text="Procesando")
        self.label_loading.config(fg="blue", font=("Cabin", 15,), width=10)

        self.x_coordenate_of_loading_points = 240
        self.after_function_id = None
        self.loading_points = Label(self, text=". . .")
        self.loading_points.config(fg="blue", font=("Courier", 15, "italic"))
        
        #text to show the scrapping result
        self.textarea_scrapping_result = Text(self)
        self.textarea_scrapping_result.config(width = 59, height = 14)
        self.textarea_scrapping_result.place(x = 10, y = 200)
        
        # Button to export scrapping results as files
        self.button_export_scrapping_results_as_files = Button(self, text="Exportar como archivos", command=self.start_exporting_as_files)
        self.button_export_scrapping_results_as_files.place(x=120, y=440)
        
        # Button to export scrapping results to idm
        self.button_export_scrapping_results_to_idm = Button(self, text="Exportar a IDM", command=self.start_exporting_to_idm)
        self.button_export_scrapping_results_to_idm.place(x=10, y=440)
        
        self.bind('<Return>', self.iniciar_scrapping)
        self.box_serie_or_temp.bind('<Return>', self.iniciar_scrapping)
        
    def iniciar_scrapping(self, event = None):
        """Start the scraping process based on the selected type of scrapping."""
        url_serie = self.input_url_serie.get()
        type_of_scrapping = self.box_serie_or_temp.get()
        
        # Check that no field is empty
        if url_serie == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        elif type_of_scrapping == self.type_of_scrapping["none"]:    
            messagebox.showinfo("!","Selecciona un tipo de Scrapping")
        else:
            # If the user wants to download a full series
            if type_of_scrapping == self.type_of_scrapping["serie"]:
                t = threading.Thread(target=self.scrapping_serie, args=[url_serie])
                t.start()   
            # If the user wants to download only one season
            else:
                t = threading.Thread(target=self.scrapping_one_temp, args=[url_serie])
                t.start() 
    
    def scrapping_serie(self, url_serie):
        """Get the links of a full series, including all seasons."""
        self.disable_buttons()
        self.show_loading_status()
        try:
            self.scrapping_results = scrapping.scrapping(url_serie, verify = self.use_https_verification.get() == 1)
            self.show_scrapping_result(self.scrapping_results)
            messagebox.showinfo("!","Operacion finalizada con éxito")
            self.enable_buttons()
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text="Reintentar")
            self.enable_buttons()
        except Exception as e:
            messagebox.showinfo("!", "Herror al obtener los links") 
            self.button.config(text="Reintentar")
            self.enable_buttons()  
        finally:
            self.hide_loading_status()      
    
    def scrapping_one_temp(self, url_serie):
        """Get the links of one season of the series."""
        self.disable_buttons()
        self.show_loading_status()
        try:
            self.scrapping_results = scrapping.get_one_temp(url_serie, verify = self.use_https_verification.get() == 1)
            self.show_scrapping_result(self.scrapping_results)
            messagebox.showinfo("!","Operacion finalizada con éxito")
            self.enable_buttons()            
        except RequestException:
            messagebox.showinfo("!", "Herror de conexion, revisa tu conexion a internet o el link de descarga")   
            self.button.config(text="Reintentar")
            self.enable_buttons()
        except Exception:
            messagebox.showinfo("!", "Herror al obtener los links")   
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
        if self.loading_points.winfo_x() >= 270:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=120, y=143)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=148)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.root.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        """Hide the loading status."""
        self.root.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()

    def show_scrapping_result(self, results):
        """
        Show the scrapping results on the log textarea for user to visualize if the output is correct.

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
        self.textarea_scrapping_result.delete(1.0, END)
        
        for show, seasons in results.items():
            self.textarea_scrapping_result.insert(END, f"{show}\n")
            
            if isinstance(seasons, dict):
                for season, links in seasons.items():
                    self.textarea_scrapping_result.insert(END, f"  -- {season}\n")
                    for link in links:
                        self.textarea_scrapping_result.insert(END, f"       • {link}\n")
            elif isinstance(seasons, list):
                for link in seasons:
                    self.textarea_scrapping_result.insert(END, f"   • {link}\n")
            else:
                self.textarea_scrapping_result.insert(END, f"   • {seasons}\n")
            
            self.textarea_scrapping_result.insert(END, "\n")
    
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
            if not self.scrapping_results:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            if not carpeta_destino:
                return
            
            for show, seasons in self.scrapping_results.items():
                carpeta_programa = os.path.join(carpeta_destino, show)
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descargar visuales)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                if isinstance(seasons, dict):
                    for season, links in seasons.items():
                        carpeta_temporada = os.path.join(carpeta_programa, season)
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
        except Exception:
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
            
            if not self.scrapping_results:
                return messagebox.showinfo("!", "No hay nada que exportar")
            
            self.label_loading.config(text="Exportando")
            self.disable_buttons()
            self.show_loading_status()
            
            carpeta_destino = filedialog.askdirectory(title="Donde desea guardar el contenido")
            if not carpeta_destino:
                return
            
            for show, seasons in self.scrapping_results.items():
                carpeta_programa = os.path.join(carpeta_destino, show)
                
                # Check if the folder already exists and add suffix if necessary
                if os.path.exists(carpeta_programa):
                    carpeta_programa += " (descarga automatica con IDM)"
                
                os.makedirs(carpeta_programa, exist_ok=True)
                
                if isinstance(seasons, dict):
                    for season, links in seasons.items():
                        carpeta_temporada = os.path.join(carpeta_programa, season)
                        os.makedirs(carpeta_temporada, exist_ok=True)
                        for link in links:
                            subprocess.run([idm_path, '/d', link, '/p', carpeta_temporada, '/n', '/a'])
                elif isinstance(seasons, list):
                    for link in seasons:
                        subprocess.run([idm_path, '/d', link, '/p', carpeta_programa, '/n', '/a'])
                else:
                    messagebox.showinfo("!Error", "Error al exportar")           
            
            messagebox.showinfo("!", "Exportación Exitosa")
        except Exception:
            messagebox.showinfo("!Error", "Error al exportar")    
        finally:    
            self.label_loading.config(text="Buscando")
            self.hide_loading_status()
            self.enable_buttons()
    
    def start_exporting_to_idm(self):
        threading.Thread(target=self.export_searching_results_to_idm).start()
    
    def start_exporting_as_files(self):    
        threading.Thread(target=self.export_searching_results_as_files).start()