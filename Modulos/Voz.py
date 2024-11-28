import pyttsx3
class Voz:
    def __init__(self):
        self.engine = pyttsx3.init()

        # Obtener las voces disponibles
        voices = self.engine.getProperty('voices')

        self.engine.setProperty('voice',2)

        # Establecer la velocidad de habla
        self.engine.setProperty('rate', 200)

    def decir_mensaje(self, contenido):
        self.engine.say(contenido)
        self.engine.runAndWait()
