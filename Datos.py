import json

class Datos:
    def __init__(self, url, identificador, usuario, contrasena):
        self.url = url
        self.identificador = identificador
        self.usuario = usuario
        self.contrasena = contrasena

    def __repr__(self):
        return (f"Datos(url={self.url}, identificador={self.identificador}, "
                f"usuario={self.usuario}, contrasena={self.contrasena})")

    @staticmethod
    def cargar_datos_json(file_path="Datos.json"):
        try:
            with open(file_path, 'r') as archivo:
                datos_dict = json.load(archivo)
                
            # Crear y devolver una instancia de Datos con los datos cargados
            return Datos(
                url=datos_dict.get("url"),
                identificador=datos_dict.get("identificador"),
                usuario=datos_dict.get("usuario"),
                contrasena=datos_dict.get("contrasena")
            )
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {file_path}")
            return None
        except json.JSONDecodeError:
            print("Error: El archivo JSON tiene un formato inválido.")
            return None

    @classmethod
    def obtenerDatos(cls, file_path="Datos.json"):
        # Cargar los datos y devolverlos como un diccionario
        instancia = cls.cargar_datos_json(file_path)
        if instancia:
            return {
                "url": instancia.url,
                "identificador": instancia.identificador,
                "usuario": instancia.usuario,
                "contrasena": instancia.contrasena
            }
        return None
        
    @staticmethod
    def guardarDatos(nuevos_datos, file_path="Datos.json"):
        try:
            # Crear un diccionario con los nuevos datos
            datos_dict = {
                "url": nuevos_datos["url"],
                "identificador": nuevos_datos["identificador"],
                "usuario": nuevos_datos["usuario"],
                "contrasena": nuevos_datos["contrasena"]
            }
            # Guardar los datos en el archivo JSON
            with open(file_path, 'w') as archivo:
                json.dump(datos_dict, archivo, indent=4)
            print("Datos guardados correctamente.")
            return True
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
            return False
