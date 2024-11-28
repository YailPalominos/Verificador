import sqlite3

class Usuario:
    def __init__(self, usuario=None, pin=None, rfid=None, nombres=None, apellidos=None,
                 direccion_correo_electronico=None, huella=None, foto=None, turno=None):
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

class UsuarioRepository:
    def __init__(self):
        self.db_name = 'Verificador.db'

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table_usuarios(self):
        with self.connect_db() as conn:
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

    def create_usuario(self, usuario, pin, rfid, nombres, apellidos,
                       direccion_correo_electronico, huella=None, foto=None, turno=None):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Usuarios (usuario, pin, rfid, nombres, apellidos,
                            direccion_correo_electronico, huella, foto, turno)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (usuario, pin, rfid, nombres, apellidos,
                            direccion_correo_electronico, huella, foto, turno))
            conn.commit()
            
    def get_all_usuarios(self):
        with self.connect_db() as conn:
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

    def get_usuario_by_usuario(self, usuario):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE usuario = ?', (usuario,))
            registro = cursor.fetchone()

            if registro:
                return Usuario(
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
            else:
                return None

    def create_multiple_usuarios(self, usuarios_nuevos):
        """Borra todos los usuarios existentes antes de agregar nuevos"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuarios")
            conn.commit()

            for usuario in usuarios_nuevos:
                cursor.execute('''INSERT INTO Usuarios (usuario, pin, rfid, nombres, apellidos,
                                direccion_correo_electronico, huella, foto, turno)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (usuario['usuario'], usuario['pin'], usuario['rfid'], usuario['nombres'],
                                usuario['apellidos'], usuario['direccion_correo_electronico'],
                                usuario.get('huella'), usuario.get('foto'), usuario.get('turno')))
            conn.commit()
            print("Nuevos usuarios creados correctamente.")

    def get_usuario_by_pin(self, pin):
        with self.connect_db() as conn:
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

    def get_usuario_by_rfid(self, rfid):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE rfid = ?', (rfid,))
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

    def get_usuario_by_foto(self, foto):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE foto = ?', (foto,))
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

    def get_usuario_by_huella(self, huella):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE huella = ?', (huella,))
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
