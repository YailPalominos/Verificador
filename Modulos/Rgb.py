import RPi.GPIO as GPIO
import time

class Rgb:
    def __init__(self):
        GPIO.setwarnings(False)
        """
        Inicializa el LED RGB con los pines predefinidos: 
        17 para rojo, 27 para verde y 22 para azul.
        """
        self.pin_red = 17
        self.pin_green = 27
        self.pin_blue = 22
        
        GPIO.setmode(GPIO.BCM)  # Establece el modo BCM de numeración de pines

        # Configura los pines como salida
        GPIO.setup(self.pin_red, GPIO.OUT)
        GPIO.setup(self.pin_green, GPIO.OUT)
        GPIO.setup(self.pin_blue, GPIO.OUT)


    def set_color(self, red, green, blue, duration=2):
        """
        Establece el color del LED RGB.
        :param red: Estado del pin rojo (True o False).
        :param green: Estado del pin verde (True o False).
        :param blue: Estado del pin azul (True o False).
        :param duration: Tiempo en segundos para mantener el color (por defecto 2 segundos).
        """
        GPIO.output(self.pin_red, red)
        GPIO.output(self.pin_green, green)
        GPIO.output(self.pin_blue, blue)
        time.sleep(duration)

        GPIO.output(self.pin_red, GPIO.LOW)
        GPIO.output(self.pin_green, GPIO.LOW)
        GPIO.output(self.pin_blue, GPIO.LOW)
