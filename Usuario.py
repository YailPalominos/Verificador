import sqlite3

# Clase Usuarios con los nuevos atributos
class Usuario:
    def __init__(self, usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico):
        self.usuario = usuario
        self.pin = pin
        self.rfid = rfid
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion_correo_electronico = direccion_correo_electronico

    def __repr__(self):
        return (f"Usuario(usuario={self.usuario}, pin={self.pin}, rfid={self.rfid}, "
                f"nombres={self.nombres}, apellidos={self.apellidos}, "
                f"direccion_correo_electronico={self.direccion_correo_electronico})")


# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Verificador.db')
cursor = conn.cursor()

# Crear tabla Usuarios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        usuario NVARCHAR(50) NOT NULL PRIMARY KEY,
        pin NVARCHAR(8),
        rfid NVARCHAR(16),
        nombres NVARCHAR(50),
        apellidos NVARCHAR(50),
        direccion_correo_electronico NVARCHAR(30)
    )
''')
conn.commit()

# Función para crear un registro en la tabla Usuarios
def create_usuario(usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico):
    cursor.execute('''
        INSERT INTO Usuarios (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico))
    conn.commit()
    print("Registro insertado en Usuarios")

# Función para obtener todos los registros de Usuarios como instancias del modelo Usuario
def get_all_usuarios():
    cursor.execute('SELECT * FROM Usuarios')
    registros = cursor.fetchall()
    
    usuarios = []
    for registro in registros:
        usuario = Usuario(
            usuario=registro[0],
            pin=registro[1],
            rfid=registro[2],
            nombres=registro[3],
            apellidos=registro[4],
            direccion_correo_electronico=registro[5]
        )
        usuarios.append(usuario)

    return usuarios


def get_usuario_by_pin(pin):
    cursor.execute('SELECT * FROM Usuarios WHERE pin = ?', (pin,))
    registro = cursor.fetchone()

    if registro:
        usuario = Usuario(
            usuario=registro[0],
            pin=registro[1],
            rfid=registro[2],
            nombres=registro[3],
            apellidos=registro[4],
            direccion_correo_electronico=registro[5]
        )
        return usuario
    else:
        return None
