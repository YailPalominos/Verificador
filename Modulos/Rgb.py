import RPi.GPIO as GPIO

# Id de la tarjeta conocida (ejemplo: reemplazar con un ID real)
ID_CONOCIDO = 596940268731  # Reemplaza con el ID de tarjeta conocido


# Configuración del LED RGB (usando los pines GPIO 26, 6 y 13)
GPIO.setup(26, GPIO.OUT)  # Rojo
GPIO.setup(6, GPIO.OUT)   # Verde
GPIO.setup(13, GPIO.OUT)  # Azul

# Inicialización de pyttsx3 para la síntesis de voz
engine = pyttsx3.init()

# Función para controlar el color del LED RGB
def set_led_rgb(red, green, blue):
    GPIO.output(26, red)  # Controla el color rojo
    GPIO.output(13, green)  # Controla el color verde
    GPIO.output(6, blue)  # Controla el color azul