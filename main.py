import tkinter as tk
from tkinter import ttk
from utils import center_window
from Series_Scrapper_Page import Series_Scrapper_Page

class Main():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visuales Scrapper")
        self.root.geometry(center_window(500, 500, self.root))
        self.root.resizable(0, 0)

        # Tabs control
        self.tabControl = ttk.Notebook(self.root)

        # Crear los frames para cada tab
        self.series_scrapper_tab = Series_Scrapper_Page(self.tabControl, root = self.root)
        self.build_database_tab = ttk.Frame(self.tabControl)
                
        # Añadir los tabs al control de tabs
        self.tabControl.add(self.series_scrapper_tab, text='Series Scrapper')
        self.tabControl.add(self.build_database_tab, text='Build Database')

        # Empaquetar el control de tabs
        self.tabControl.pack(expand=1, fill="both")
        
        self.label2 = tk.Label(self.build_database_tab, text="Contenido del Tab 2")
        self.label2.pack(pady=10, padx=10)

        # Iniciar el bucle principal de la aplicación
        self.root.mainloop()

Main()