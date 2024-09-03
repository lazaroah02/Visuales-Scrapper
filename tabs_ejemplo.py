import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de Tabs con Tkinter")

# Crear el control de tabs
tabControl = ttk.Notebook(root)

# Crear los frames para cada tab
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

# Añadir los tabs al control de tabs
tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')

# Empaquetar el control de tabs
tabControl.pack(expand=1, fill="both")

# Añadir contenido a los tabs
label1 = tk.Label(tab1, text="Contenido del Tab 1")
label1.pack(pady=10, padx=10)

label2 = tk.Label(tab2, text="Contenido del Tab 2")
label2.pack(pady=10, padx=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()
