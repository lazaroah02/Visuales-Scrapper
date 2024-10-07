import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from pages.Specific_Media_Scrapper_Page import SpecificMediaScrapperPage
from utils.utils import center_window
from pages.Build_Database_Page import BuildDatabasePage
from pages.Search_Page import SearchPage
import os
from utils.toast import Toast

class Main():
    def __init__(self):
        """Initialize the main application window and tabs."""
        self.root = tk.Tk()
        self.root.title("Visuales Scrapper")
        self.root.geometry(center_window(500, 500, self.root))
        self.root.resizable(0, 0)
        
        self.stop_program = False
        
        #logo
        self.absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
        self.icon_path = os.path.join(self.absolute_folder_path, './logo.png')
        self.icon = PhotoImage(file = self.icon_path)
        self.root.iconphoto(True, self.icon)

        # Tabs control
        self.tabControl = ttk.Notebook(self.root)

        # Create frames for each tab
        self.search_tab = SearchPage(self.tabControl, check_if_program_stoped = self.check_if_program_stoped)
        self.build_database_tab = BuildDatabasePage(self.tabControl, check_if_program_stoped = self.check_if_program_stoped)
        self.scrape_specific_media_tab = SpecificMediaScrapperPage(self.tabControl, check_if_program_stoped = self.check_if_program_stoped)
                
        # Add tabs to the tab control
        self.tabControl.add(self.search_tab, text='Search in Database')
        self.tabControl.add(self.build_database_tab, text='Build Database')
        self.tabControl.add(self.scrape_specific_media_tab, text='Scrape Specific Media')

        # Pack the tab control
        self.tabControl.pack(expand=1, fill="both")
        
        # Configure closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the main application loop
        self.root.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            self.stop_program = True
            self.root.after(3000, self.root.destroy)
            Toast(self.root, "Cerrando", "Cerrando programa ...")
    
    def check_if_program_stoped(self):
        return self.stop_program            

Main()
