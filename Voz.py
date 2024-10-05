import pyttsx3

# Inicializar el motor de TTS
engine = pyttsx3.init()

# Obtener las voces disponibles
voices = engine.getProperty('voices')

# Seleccionar una voz (por ejemplo, la primera)
engine.setProperty('voice', voices[0].id)

# Establecer la velocidad (rate) más lenta
engine.setProperty('rate', 170)  # La velocidad estándar es 200, menor es más lento

# Definir la cadena que quieres que se lea en voz alta
cadena = "Buen día,Braulio Yail"

# Hacer que el motor diga la cadena
engine.say(cadena)

# Ejecutar el motor para que hable
engine.runAndWait()

