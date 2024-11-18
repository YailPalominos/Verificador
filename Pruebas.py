import sqlite3

# Función para conectar a la base de datos
def connect_db():
    return sqlite3.connect('Verificador.db')

# Función para insertar un nuevo usuario en la tabla
def create_usuario(usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella=None, foto=None, turno=None):
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Insertar el nuevo usuario en la tabla Usuarios
        cursor.execute('''INSERT INTO Usuarios (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella, foto, turno)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella, foto, turno))
        conn.commit()
        print("Nuevo usuario creado.")

# # Ejemplo de uso: Crear un usuario
# create_usuario(
#     usuario="1",
#     pin="12345",
#     rfid="596940268731",
#     nombres="John",
#     apellidos="Doe",
#     direccion_correo_electronico="jdoe@example.com",
#     huella=None,  # Si tienes huella, aquí puedes poner un objeto binario
#     foto=None,    # Lo mismo para la foto
#     turno=1       # Asumiendo que "1" es un turno válido
# )
