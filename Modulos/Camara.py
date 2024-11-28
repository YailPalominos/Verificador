import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camara:
    def __init__(self, parent):
        self.parent = parent

        # Configurar la camara de Raspberry Pi
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(1280, 720))

        # Cargar el clasificador en cascada de OpenCV para detectar rostros
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Crear un label para mostrar el feed de la camara
        self.label = tk.Label(parent)
        self.label.pack()

        # Crear un label para el reloj
        self.reloj_label = tk.Label(parent, font=("Helvetica", 20), bg="black", fg="white")
        self.reloj_label.pack()
        self.mensaje_label = tk.Label(parent, font=("Helvetica", 20), fg="red", bg="black")
        self.mensaje_label.pack()
        self.mensaje_label.config(text="")

    def iniciar_transmision(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                self.mensaje_label.config(text="Rostro detectado!")
            else:
                self.mensaje_label.config(text="")

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (800, 480))
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            self.rawCapture.truncate(0)
            break

        self.mostrar_reloj()
        self.parent.after(10, self.iniciar_transmision)

    def mostrar_reloj(self):
        fecha_hora_actual = time.strftime('%Y-%m-%d %H:%M:%S')
        self.reloj_label.config(text=fecha_hora_actual)
        self.centrar_reloj()

    def centrar_reloj(self):
        ventana_ancho = self.parent.winfo_width()
        reloj_ancho = self.reloj_label.winfo_width()
        posicion_x = (ventana_ancho - reloj_ancho) // 2
        self.reloj_label.place(x=posicion_x, y=10)

    def cerrar(self):
        self.camera.close()
