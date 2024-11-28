import threading
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time
from Autenticar import Autenticar

class Rfid:
    
    def __init__(self):
        GPIO.setwarnings(False)
        self.reader = SimpleMFRC522()
        self.running = False  # Controla el hilo    
        self.thread = None
        self.autenticar = Autenticar(None)
        
    def iniciar_lectura(self):
        """Lee una tarjeta RFID y procesa el UID"""
        try:
            uid, _ = self.reader.read()
            self.autenticar.autenticar_rfid(uid)
            print(f"UID detectado: {uid}")
            
        except Exception as e:
            print(f"Error al leer RFID: {e}")

    def _leer_continuamente(self):
        while self.running:
            self.iniciar_lectura()
            time.sleep(1)

    def iniciar_hilo(self):
        """Inicia el hilo de lectura continua"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._leer_continuamente)
            self.thread.start()
            print("Lectura RFID iniciada")

    def detener_hilo(self):
        """Detiene el hilo de lectura continua"""
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
            GPIO.cleanup()  # Libera los pines GPIO al finalizar
            print("Lectura RFID detenida.")
