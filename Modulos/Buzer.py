import RPi.GPIO as GPIO
import time

buzzer_pwm = GPIO.PWM(8, 440)  # Frecuencia inicial de 440 Hz}

class Buzer:
    def __init__():
        GPIO.setup(8, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)

    def _emitir_sonido(frecuencia, duracion):
        """
        Emite un sonido con la frecuencia y duración dadas.
        La frecuencia está en Hertz (Hz), y la duración está en segundos.
        """
        pwm = GPIO.PWM(buzzer_pwm.pin, frecuencia)  # Genera una señal PWM con la frecuencia
        pwm.start(50)  # 50% de ciclo de trabajo
        time.sleep(duracion)  # Emite el sonido durante la duración
        pwm.stop()  # Detiene el sonido

    def error():
        """
        Emite un sonido para indicar un error (frecuencia y duración apropiada para error).
        """
        self._emitir_sonido(1000, 0.5)  # Sonido corto y de baja frecuencia para error

    def listo():
        """
        Emite un sonido para indicar que todo está listo (frecuencia y duración apropiada para listo).
        """
        self._emitir_sonido(2000, 0.3)  # Sonido más alto y corto para listo
