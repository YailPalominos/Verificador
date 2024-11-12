import tkinter as tk
from tkinter import ttk
from Camara import Camara
from Pin import Pin
from Administrador import Administrador

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana principal")
        
        # Configuramos el tamaño fijo de la ventana
        self.root.geometry("800x480")
        
        # Quitar bordes de la ventana principal
        self.root.config(bd=0, highlightthickness=0)

        # Crear un Notebook (pestañas) dentro de la ventana principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Crear las pestañas
        pestania1 = tk.Frame(self.notebook, bg="#222222")
        pestania2 = tk.Frame(self.notebook, bg="#222222")
        pestania3 = tk.Frame(self.notebook, bg="#222222")

        # Agregar las pestañas al Notebook
        self.notebook.add(pestania1, text="•")
        self.notebook.add(pestania2, text="•")
        self.notebook.add(pestania3, text="•")

        # Crear la cámara y agregarla a la primera pestaña
        self.camara = Camara(pestania1)
        self.camara.iniciar_transmision()
        
        self.pin = Pin(pestania2)
        self.pin.crear_interfaz()
        
        self.administrador = Administrador(pestania3)

# Crear la ventana principal
root = tk.Tk()

# Crear la instancia de la clase VentanaPrincipal
ventana = VentanaPrincipal(root)

# Iniciar el bucle de la aplicación
root.mainloop()