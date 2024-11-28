import RPi.GPIO as GPIO
import time

class Buzer:
    buzzer_pwm = None

    def __init__(self):
        """Inicializa el buzzer en el pin 13 y configura la frecuencia inicial."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)  # Configura el pin 13 como salida

        if Buzer.buzzer_pwm is None:
            Buzer.buzzer_pwm = GPIO.PWM(13, 440)  # Frecuencia inicial de 440 Hz
            Buzer.buzzer_pwm.start(0)  # Inicia el PWM con ciclo de trabajo en 0%

    def _emitir_sonido(self, frecuencia, duracion):
        
        Buzer.buzzer_pwm.ChangeFrequency(frecuencia)  # Cambia la frecuencia del PWM
        Buzer.buzzer_pwm.ChangeDutyCycle(50)  # 50% de ciclo de trabajo
        time.sleep(duracion)  # Emite el sonido durante la durac
        Buzer.buzzer_pwm.ChangeDutyCycle(0)  # Detiene el sonido

    def error(self):
        self._emitir_sonido(1000, 0.5)  # Sonido corto y de baja frecuencia para error

    def correcto(self):
        self._emitir_sonido(2000, 0.3)  # Sonido mas alto y corto para correcto
