import threading
from tkinter import Checkbutton, Entry, Button, Label, IntVar, messagebox, filedialog, ttk
import functionalities.scrapping as scrapping
from requests import RequestException

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

        # Label for input URL of the series
        self.label_url_serie = Label(self, text="URL de la serie")
        self.label_url_serie.place(x=10, y=20)

        # Input for the series URL
        self.input_url_serie = Entry(self)
        self.input_url_serie.config(width=50)
        self.input_url_serie.place(x=100, y=20)
        
        #checkbox remember database
        self.checkbox_use_https_verification = Checkbutton(self, variable=self.use_https_verification, text="Usar verificación https", onvalue=1, offvalue=0)
        self.checkbox_use_https_verification.place(x=6, y=50)

        # Label for destination folder
        self.label_ruta_destino = Label(self, text="Ruta de destino")
        self.label_ruta_destino.place(x=10, y=90)

        # Input for the destination folder path
        self.input_ruta_destino = Entry(self)
        self.input_ruta_destino.config(width=50)
        self.input_ruta_destino.place(x=100, y=90)

        # Button to select the destination folder path
        self.button_select_ruta = Button(self, text="Seleccionar", command=self.seleccionar_ruta_destino)
        self.button_select_ruta.place(x=420, y=85)

        self.type_of_scrapping = {
            "none": "Tipo de Scrapping",
            "serie": "Serie Completa",
            "temp": "Temporada",
        }

        # Combobox to select whether to download a full series or a season
        self.box_serie_or_temp = ttk.Combobox(self, text="Tipo de Scrapping", state="readonly",
                                              values=[self.type_of_scrapping["serie"], self.type_of_scrapping["temp"]])
        self.box_serie_or_temp.set(self.type_of_scrapping["none"])
        self.box_serie_or_temp.config(width=30)
        self.box_serie_or_temp.place(x=15, y=150)

        # Button to start scraping for a series
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
        """Open a dialog to select the destination folder and update the input field."""
        self.input_ruta_destino.delete(0, "end")
        path = str(filedialog.askdirectory())
        self.input_ruta_destino.insert(0, path)
        
    def iniciar_scrapping(self):
        """Start the scraping process based on the selected type of scrapping."""
        url_serie = self.input_url_serie.get()
        ruta_destino = self.input_ruta_destino.get()
        type_of_scrapping = self.box_serie_or_temp.get()
        
        # Check that no field is empty
        if url_serie == "" or ruta_destino == "":
            messagebox.showinfo("!","No pueden haber campos vacios")
        elif type_of_scrapping == self.type_of_scrapping["none"]:    
            messagebox.showinfo("!","Selecciona un tipo de Scrapping")
        else:
            # If the user wants to download a full series
            if type_of_scrapping == self.type_of_scrapping["serie"]:
                t = threading.Thread(target=self.scrapping_serie, args=[url_serie, ruta_destino])
                t.start()   
            # If the user wants to download only one season
            else:
                t = threading.Thread(target=self.scrapping_one_temp, args=[url_serie, ruta_destino])
                t.start() 
    
    def scrapping_serie(self, url_serie, ruta_destino):
        """Get the links of a full series, including all seasons."""
        self.disable_buttons()
        self.show_loading_status()
        try:
            scrapping.scrapping(url_serie, ruta_destino, verify = self.use_https_verification.get() == 1)
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
    
    def scrapping_one_temp(self, url_serie, ruta_destino):
        """Get the links of one season of the series."""
        self.disable_buttons()
        self.show_loading_status()
        try:
            scrapping.get_one_temp(url_serie, ruta_destino, verify = self.use_https_verification.get() == 1)
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
        self.button_select_ruta.config(state="normal")
        
    def disable_buttons(self):
        """Disable the buttons in the UI."""
        self.button.config(state="disabled")
        self.button_select_ruta.config(state="disabled")
    
    def show_loading_status(self, frame=0):
        """Show the loading status with an animated effect."""
        if self.loading_points.winfo_x() >= 270:
            self.loading_points.place(x=self.x_coordenate_of_loading_points)
            frame = 0
        # Update the position of the loading point
        self.label_loading.place(x=120, y=200)     
        self.loading_points.place(x=(self.x_coordenate_of_loading_points + frame), y=200)
        # Schedule the next frame to be displayed after 250 milliseconds
        self.after_function_id = self.root.after(250, self.show_loading_status, frame + 5)
    
    def hide_loading_status(self):
        """Hide the loading status."""
        self.root.after_cancel(self.after_function_id)
        self.label_loading.place_forget()    
        self.loading_points.place_forget()
