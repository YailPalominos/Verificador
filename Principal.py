import tkinter as tk
from tkinter import ttk
#from Modulos.Camara import Camara
from Modulos.Pin import Pin
from Modulos.Huella import Huella
from Modulos.Rfid import Rfid
from Administrador import Administrador
from Modulos.Recepcion import Recepcion
import threading

class Principal:
        
    def __init__(self, root):
        self.root = root
        self.root.title("Controlador de permanencia")
        
        self.root.attributes('-fullscreen', True)
        
        self.root.bind("<Escape>", self.salir_fullscreen)
        
        # Configuramos el tamaño fijo de la ventana
        #self.root.geometry("800x480")
        
        # Quitar bordes de la ventana principal
        self.root.config(bd=0, highlightthickness=0)

        # Crear un Notebook (pestañas) dentro de la ventana principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Crear las pestañas
        #pestania1 = tk.Frame(self.notebook, bg="#222222")
        pestania2 = tk.Frame(self.notebook, bg="#222222")
        pestania3 = tk.Frame(self.notebook, bg="#222222")

        # Agregar las pestañas al Notebook
        #self.notebook.add(pestania1, text=".")
        self.notebook.add(pestania2, text=".")
        self.notebook.add(pestania3, text=".")

        # Crear la camara y agregarla a la primera pestaña
        #self.camara = Camara(pestania1)
        #self.camara.iniciar_transmision()
        
        self.pin = Pin(pestania2)
        self.pin.crear_interfaz()
        
        self.administrador = Administrador(pestania3)
        
        self.recepcion = Recepcion()
        self.recepcion.start()
        
        self.rfid = Rfid()
        self.rfid_thread = threading.Thread(target=self.rfid.iniciar_hilo, daemon=True)
        self.rfid_thread.start()
        
        #huella = Huella()
        #huella_thread = threading.Thread(target=huella.iniciar, daemon=True)
        #huella_thread.start()
        
    def salir_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("800x480")

# Crear la ventana principal
root = tk.Tk()

# Crear la instancia de la clase Principal
ventana = Principal(root)

# Iniciar el bucle de la aplicacion
root.mainloop()
