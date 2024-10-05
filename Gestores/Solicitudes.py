import pyttsx3

def iniciar_motor_tts():
    # Inicializar el motor de TTS
    engine = pyttsx3.init()
    return engine

def listar_voces(engine):
    # Obtener las voces disponibles
    voices = engine.getProperty('voices')
    
    # Mostrar las voces disponibles
    for index, voice in enumerate(voices):
        print(f"Voz {index}:")
        print(f" - ID: {voice.id}")
        print(f" - Nombre: {voice.name}")
        print(f" - Idioma: {voice.languages}")
        print(f" - Género: {voice.gender}")
        print(f" - Edad: {voice.age}")
        print()
    
    return voices

def seleccionar_voz(engine, voz_index):
    voices = listar_voces(engine)
    if voices:  # Verifica que haya voces disponibles
        engine.setProperty('voice', voices[voz_index].id)
    else:
        print("No hay voces disponibles.")

def hablar(engine, cadena):
    # Establecer la velocidad (rate) más lenta
    engine.setProperty('rate', 170)  # La velocidad estándar es 200, menor es más lento

    # Hacer que el motor diga la cadena
    engine.say(cadena)

    # Ejecutar el motor para que hable
    engine.runAndWait()

if __name__ == "__main__":
    # Cadena que quieres que se lea en voz alta
    cadena = "No quiero ir, ¡ayuda!"

    # Iniciar el motor TTS
    engine = iniciar_motor_tts()

    # Seleccionar una voz (puedes cambiar el índice según la voz que desees usar)
    seleccionar_voz(engine, 0)  # Cambia 0 al índice deseado si es necesario

    # Hablar la cadena definida
    hablar(engine, cadena)
