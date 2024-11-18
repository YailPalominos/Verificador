import pyttsx3

class Voz:
    def __init__(self):
        # Inicializar el motor de TTS
        self.engine = pyttsx3.init()

        # Obtener las voces disponibles
        voices = self.engine.getProperty('voices')
        
        # Seleccionar una voz en particular
        if len(voices) > 3:
            self.engine.setProperty('voice', voices[3].id)
        else:
            self.engine.setProperty('voice', voices[0].id)  # Por si la voz 3 no está disponible

        # Establecer la velocidad de habla
        self.engine.setProperty('rate', 170)  # Ajusta la velocidad de lectura

    def decir_mensaje(self, contenido):
        # Pasar el contenido al motor para que lo lea
        self.engine.say(contenido)

        # Ejecutar el motor para que hable
        self.engine.runAndWait()
