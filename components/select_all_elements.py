from tkinter import ttk, IntVar

class SelectAllElements(ttk.Checkbutton):
    def __init__(self, parent, text = "Seleccionar Todos", elements_to_select = []):
        self.selected = IntVar(value = 1)
        self.elements_to_select = elements_to_select
        super().__init__(parent, variable=self.selected, onvalue=1, offvalue=0, text = text, command=self.on_change)
    
    def on_change(self):
        for element in self.elements_to_select:
            if self.selected.get() == 1:
                element.selected.set(1)
            else:
                element.selected.set(0)