import tkinter as tk
from utils.utils import center_window

class Toast:
    def __init__(self, root, title, message, duration = 3000):
        # Crear la ventana principal
        self.top = tk.Toplevel(root)
        self.top.title(title)
        self.top.geometry(center_window(250, 100, self.top))

        # Crear una etiqueta con el mensaje
        message_label = tk.Label(self.top, text=message)
        message_label.pack(pady=20)

        # Configurar la ventana para que se cierre después de 3 segundos (3000 milisegundos)
        self.top.after(duration, self.close_toplevel)

        # Ejecutar el bucle principal de la interfaz gráfica
        self.top.mainloop()
    
    def close_toplevel(self):
        self.top.destroy()    
