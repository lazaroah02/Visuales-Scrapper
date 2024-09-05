import tkinter as tk
from tkinter import PhotoImage, ttk
from utils.utils import center_window
from pages.Series_Scrapper_Page import SeriesScrapperPage
from pages.Build_Database_Page import BuildDatabasePage
from pages.Search_Page import SearchPage
import os

class Main():
    def __init__(self):
        """Initialize the main application window and tabs."""
        self.root = tk.Tk()
        self.root.title("Visuales Scrapper")
        self.root.geometry(center_window(500, 500, self.root))
        self.root.resizable(0, 0)
        
        #logo
        self.absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
        self.icon_path = os.path.join(self.absolute_folder_path, './logo.png')
        self.icon = PhotoImage(file = self.icon_path)
        self.root.iconphoto(True, self.icon)

        # Tabs control
        self.tabControl = ttk.Notebook(self.root)

        # Create frames for each tab
        self.series_scrapper_tab = SeriesScrapperPage(self.tabControl, root=self.root)
        self.build_database_tab = BuildDatabasePage(self.tabControl, root=self.root)
        self.search_tab = SearchPage(self.tabControl, root=self.root)
                
        # Add tabs to the tab control
        self.tabControl.add(self.search_tab, text='Search in Database')
        self.tabControl.add(self.build_database_tab, text='Build Database')
        self.tabControl.add(self.series_scrapper_tab, text='Series Scrapper')

        # Pack the tab control
        self.tabControl.pack(expand=1, fill="both")

        # Start the main application loop
        self.root.mainloop()

Main()
