import RPi.GPIO as GPIO
import time

class Buzer:
    def __init__(self, pin):
        # Configuración del pin GPIO
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  # Usamos la numeración de pines BCM
        GPIO.setup(self.pin, GPIO.OUT)  # Configuramos el pin como salida

    def _emitir_sonido(self, frecuencia, duracion):
        """
        Emite un sonido con la frecuencia y duración dadas.
        La frecuencia está en Hertz (Hz), y la duración está en segundos.
        """
        pwm = GPIO.PWM(self.pin, frecuencia)  # Genera una señal PWM con la frecuencia
        pwm.start(50)  # 50% de ciclo de trabajo
        time.sleep(duracion)  # Emite el sonido durante la duración
        pwm.stop()  # Detiene el sonido

    def error(self):
        """
        Emite un sonido para indicar un error (frecuencia y duración apropiada para error).
        """
        self._emitir_sonido(1000, 0.5)  # Sonido corto y de baja frecuencia para error

    def listo(self):
        """
        Emite un sonido para indicar que todo está listo (frecuencia y duración apropiada para listo).
        """
        self._emitir_sonido(2000, 0.3)  # Sonido más alto y corto para listo
