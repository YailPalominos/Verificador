import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk

class Camara:
    def __init__(self, parent):
        self.parent = parent
        self.cap = cv2.VideoCapture(0)  # Inicia la cámara

        # Establecer un tamaño mayor para el campo de visión de la cámara (ángulo más grande)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Aumentamos el ancho de la imagen
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Aumentamos la altura de la imagen

        # Crear un label para mostrar el feed de la cámara
        self.label = tk.Label(parent)
        self.label.pack()

        # Crear un label para mostrar el reloj (superpuesto sobre la imagen)
        self.reloj_label = tk.Label(parent, font=("Helvetica", 20), bg="black", fg="white")
        self.reloj_label.pack()  # Lo agregamos al contenedor pero sin usar place aún

    def iniciar_transmision(self):
        """Inicia la transmisión de la cámara y la actualización del reloj"""
        ret, frame = self.cap.read()
        if ret:
            # Convierte el frame a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Redimensionamos la imagen para que se ajuste al canvas de 800x480
            frame = cv2.resize(frame, (800, 480))  # Ajustamos la imagen al tamaño deseado

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        # Actualiza el reloj
        self.mostrar_reloj()

        # Programa una nueva actualización
        self.parent.after(10, self.iniciar_transmision)

    def mostrar_reloj(self):
        """Actualiza el reloj con la fecha y hora actuales"""
        # Obtén la fecha y hora actual
        fecha_hora_actual = time.strftime('%Y-%m-%d %H:%M:%S')

        # Actualiza el label con la fecha y hora
        self.reloj_label.config(text=fecha_hora_actual)

        # Centramos el reloj en la parte superior
        self.centrar_reloj()

    def centrar_reloj(self):
        """Centrar el reloj en la parte superior"""
        # Obtiene el tamaño de la ventana
        ventana_ancho = self.parent.winfo_width()
        ventana_alto = self.parent.winfo_height()

        # Obtiene el tamaño del texto del reloj
        reloj_ancho = self.reloj_label.winfo_width()

        # Calculamos la posición horizontal para centrar el reloj
        posicion_x = (ventana_ancho - reloj_ancho) // 2

        # Colocamos el reloj en la posición calculada
        self.reloj_label.place(x=posicion_x, y=10)

    def cerrar(self):
        """Libera la cámara cuando se cierra la aplicación"""
        self.cap.release()
