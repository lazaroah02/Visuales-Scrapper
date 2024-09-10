from tkinter import ttk, IntVar

class Selectable(ttk.Checkbutton):
    def __init__(self, parent, text):
        self.selected = IntVar(value = 0)
        super().__init__(parent, variable=self.selected, onvalue=1, offvalue=0, text = text)