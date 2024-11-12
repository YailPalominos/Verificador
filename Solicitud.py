import requests
from datetime import datetime
from Verificacion import actualizar_id_verificacion

# Función para crear múltiples registros en la tabla Verificaciones
def emitir_multiples_verificaciones(url, verificaciones):
    payload = []
    
    # Construir los datos del JSON para la solicitud
    for verificacion in verificaciones:
        # Asegurarse de que la fecha esté en el formato correcto
        if 'fecha' in verificacion:
            # Convertir la fecha a formato adecuado (YYYY-MM-DDTHH:MM:SS)
            try:
                fecha = datetime.strptime(verificacion['fecha'], '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha.strftime('%Y-%m-%dT%H:%M:%S')  # Formato ISO 8601
            except ValueError:
                print(f"Error al formatear la fecha: {verificacion['fecha']}")
                fecha_formateada = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')  # En caso de error, usar la fecha actual
        else:
            fecha_formateada = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')  # Si no hay fecha, usar la fecha actual
        
        # Añadir un nuevo diccionario con el formato esperado por el servidor
        payload.append({
            'id': 0,  # Enviar id como 0, porque el servidor lo asigna
            'fecha': fecha_formateada,  # Usar la fecha formateada
            'verificador': verificacion.get('verificador', 1),  # Usar el valor del verificador
            'idVerificador': str(verificacion['id_verificador']),  # Usar el valor de id_verificador, como string
            'usuario': verificacion['usuario'],
            'tipo': verificacion['tipo'],
            'categoria': verificacion.get('categoria', None)  # Asegurarse de enviar None si no existe
        })

    try:
        # Realizar la solicitud POST al endpoint de creación múltiple
        response = requests.post(url, json=payload)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 201:
            print("Solicitud POST exitosa:", response.json())
            # Leer la respuesta del servidor para obtener los datos y el id asignado
            respuesta = response.json()
            datos = respuesta.get("datos", [])
            
            # Actualizar las verificaciones en la base de datos con los datos devueltos por el servidor
            for verificacion, data in zip(verificaciones, datos):
                id_asignado = int(data['id'])  # Convertir id a entero
                actualizar_id_verificacion(verificacion['id_verificador'], id_asignado)  # Actualizar con el nuevo id asignado
                
        else:
            print(f"Error en la solicitud POST: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud POST: {e}")