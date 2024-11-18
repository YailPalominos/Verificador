import sqlite3

class Usuario:
    def __init__(self, usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella=None, foto=None, turno=None):
        self.usuario = usuario
        self.pin = pin
        self.rfid = rfid
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion_correo_electronico = direccion_correo_electronico
        self.huella = huella
        self.foto = foto
        self.turno = turno

    def __repr__(self):
        return (f"Usuario(usuario={self.usuario}, pin={self.pin}, rfid={self.rfid}, "
                f"nombres={self.nombres}, apellidos={self.apellidos}, "
                f"direccion_correo_electronico={self.direccion_correo_electronico}, "
                f"huella={self.huella}, foto={self.foto}, turno={self.turno})")

def connect_db():
    return sqlite3.connect('Verificador.db')

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                            usuario TEXT NOT NULL PRIMARY KEY,
                            pin TEXT(8),
                            rfid TEXT(16),
                            nombres TEXT,
                            apellidos TEXT,
                            direccion_correo_electronico TEXT(30),
                            huella BLOB,
                            foto BLOB,
                            turno INTEGER
                        )''')
        conn.commit()

def create_usuario(usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella=None, foto=None, turno=None):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Usuarios (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella, foto, turno)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (usuario, pin, rfid, nombres, apellidos, direccion_correo_electronico, huella, foto, turno))
        conn.commit()
    print("Registro insertado en Usuarios")

def get_all_usuarios():
    with connect_db() as conn:
        cursor = conn.cursor()
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
                direccion_correo_electronico=registro[5],
                huella=registro[6],
                foto=registro[7],
                turno=registro[8]
            )
            usuarios.append(usuario)

    return usuarios

def get_usuario_by_pin(pin):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE pin = ?', (pin,))
        registro = cursor.fetchone()

        if registro:
            usuario = Usuario(
                usuario=registro[0],
                pin=registro[1],
                rfid=registro[2],
                nombres=registro[3],
                apellidos=registro[4],
                direccion_correo_electronico=registro[5],
                huella=registro[6],
                foto=registro[7],
                turno=registro[8]
            )
            return usuario
        else:
            return None

