import tkinter as tk
from tkinter import ttk

from components.select_all_elements import SelectAllElements
from .selectable import Selectable

class CollapsiblePane(ttk.Frame):
    """
    A class to create a collapsible pane widget using Tkinter and ttk.
    """

    # Constants for the text displayed on the toggle button
    EXPANDED_TEXT = "^"
    COLLAPSED_TEXT = ">"

    def __init__(self, parent, update_scrollregion, title=""):
        """
        Initialize the CollapsiblePane.

        Parameters:
        parent (tk.Widget): The parent widget.
        update_scrollregion (function): A function to update the scroll region when the pane is expanded or collapsed.
        """
        super().__init__(parent)
        # Function to update the scroll on CollapsiblePane expand
        self.update_scrollregion = update_scrollregion
        
        # title
        self.title = title
        
        #list of selectable_children of the pane
        self.selectable_children = []

        # Variable to control if the collapsible pane is collapsed or expanded
        self.collapsed = False

        # Variable to check if the pane is selected or not
        self.selected = tk.IntVar(value=1)

        # Create a select button to select this CollapsiblePane
        self.checkbutton = ttk.Checkbutton(self, text=None, variable=self.selected, onvalue=1, offvalue=0, command = self.on_select)
        self.checkbutton.grid(row=0, column=0, sticky="w")

        # Create a Button to toggle the pane
        self.button_toggle_pane = ttk.Button(
            self,
            text=self.EXPANDED_TEXT,
            command=self._activate,
        )
        self.button_toggle_pane.config(width=3)
        self.button_toggle_pane.grid(row=0, column=1, sticky="w")

        # Label to show the Title
        self.label_title = ttk.Label(self, text=title)
        self.label_title.grid(row=0, column=2, sticky="ew")

        # Configure the grid columns
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Create a frame to hold the content of the collapsible pane
        self.content_container = ttk.Frame(self)
        
        # create the select all elements for this Collapsible Pane
        self.select_all_elements = SelectAllElements(self.content_container)
        self.select_all_elements.grid(row=1, column=0, sticky="w", padx=10)

        # Activate the pane (set initial state)
        self._activate()

    def _activate(self):
        """
        Activate or deactivate the collapsible pane based on its current state.
        """
        if not self.collapsed:
            # If the pane is collapsed, hide the frame
            self.content_container.grid_forget()
            self.button_toggle_pane.configure(text=self.COLLAPSED_TEXT)
            self.collapsed = not self.collapsed
        else:
            # If the pane is expanded, show the frame
            self.content_container.grid(row=1, column=0, columnspan=3, sticky="w")
            self.button_toggle_pane.configure(text=self.EXPANDED_TEXT)
            self.collapsed = not self.collapsed

        # Update the scroll region
        self.update_scrollregion()
    
    def on_select(self):
        """Activate or deactivate selectable_children of the pane"""
        for child in self.selectable_children:
            if self.selected.get() == 1:
                child.selected.set(1)
            else:
                child.selected.set(0) 
        self.select_all_elements.selected.set(0) if self.selected.get() == 0 else self.select_all_elements.selected.set(1)                 

    def add_child(self, new_child):
        self.selectable_children.append(new_child)
        self.select_all_elements.elements_to_select.append(new_child)