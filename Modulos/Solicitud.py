import requests
from datetime import datetime
from Repositorios.VerificacionRepository import VerificacionRepository
from datetime import datetime
import requests
from Repositorios.VerificacionRepository import VerificacionRepository

def emitir_multiples_verificaciones(url, verificaciones):
    payload = []
    print(verificaciones)
    
    # Iterar sobre los objetos Verificacion
    for verificacion in verificaciones:
  
        if verificacion.fecha:
            # Verificar si la fecha es un objeto datetime o una cadena
            if isinstance(verificacion.fecha, str):
                try:
                    # Convertir la fecha de cadena a datetime
                    fecha = datetime.strptime(verificacion.fecha, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f"Error al formatear la fecha de cadena: {verificacion.fecha}")
                    fecha = datetime.now()  # Si la fecha no es
            else:
                # Si ya es un objeto datetime, utilizarlo directamente
                fecha = verificacion.fecha

            # Convertir a formato adecuado (YYYY-MM-DDTHH:MM:SS)
            fecha_formateada = fecha.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # Si no tiene fecha, usar la fecha actual
            fecha_formateada = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    
        payload.append({
            'id': 0,  # Enviar id como 0, porque el servidor lo asigna
            'fecha': fecha_formateada,  # Usar la fecha formateada
            'verificador': verificacion.verificador if verificacion.verificador else 1,  # Usar el valor del verificador
            'idVerificador': str(verificacion.id_verificador),  # Usar el valor de id_verificador, como string
            'usuario': verificacion.usuario,
            'tipo': verificacion.tipo,
            'categoria': verificacion.categoria if verificacion.categoria else None  # Asegurarse de enviar None si no existe
        })

    try:
       
        response = requests.post(url, json=payload)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 201:
            print("Solicitud POST exitosa:", response.json())
            # Leer la respuesta del servidor para obtener los datos y el id asignado
            respuesta = response.json()
            datos = respuesta.get("datos", [])

            repositorio_verificacion = VerificacionRepository()
            # Actualizar las verificaciones en la base de datos con los datos devueltos por el servidor
            for verificacion, data in zip(verificaciones, datos):
                id_asignado = int(data['id'])  # Convertir id a entero
                repositorio_verificacion.actualizar_id_verificacion(verificacion.id_verificador, id_asignado)  # Actualizar con el nuevo id asignado

        else:
            print(f"Error en la solicitud POST: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud POST: {e}")
