from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

# SDA -> GPIO8 (pin 24)
# SCK -> GPIO11 (pin 23)
# MOSI -> GPIO10 (pin 19)
# MISO -> GPIO9 (pin 21)
# IRQ -> No se conecta
# GND -> Ground (pin 6 o pin 14)
# RST -> GPIO25 (pin 22)
# 3.3V -> 3.3V (pin 1)

class RFIDAuth:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
        # Lista de UIDs de tarjetas autorizadas
        self.autorizados = ["123456789", "987654321"]  # Reemplaza estos valores por los UIDs de tus tarjetas

    def leer_uid(self):
        """Lee el UID de la tarjeta RFID"""
        try:
            print("Acerque su tarjeta al lector...")
            uid, text = self.reader.read()
            uid_str = str(uid)
            print(f"UID detectado: {uid_str}")
            return uid_str
        except Exception as e:
            print(f"Error al leer el RFID: {e}")
            return None

    def autenticar(self):
        """Autentica el UID leído contra la lista de autorizados"""
        uid = self.leer_uid()
        if uid in self.autorizados:
            print("Acceso permitido")
            return True
        else:
            print("Acceso denegado")
            return False

    def limpiar(self):
        """Limpia los pines GPIO al finalizar"""
        GPIO.cleanup()
