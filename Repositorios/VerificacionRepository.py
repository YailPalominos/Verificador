import sqlite3
from datetime import datetime

class Verificacion:
    def __init__(self, id_verificador=None, id=None, fecha=None, verificador=None, usuario=None, tipo=None, categoria=None):
        self.id_verificador = id_verificador
        self.id = id
        self.fecha = fecha
        self.verificador = verificador
        self.usuario = usuario
        self.tipo = tipo
        self.categoria = categoria

    def __repr__(self):
        return (f"Verificacion(id_verificador={self.id_verificador}, id={self.id}, fecha={self.fecha}, "
                f"verificador={self.verificador}, usuario={self.usuario}, tipo={self.tipo}, categoria={self.categoria})")

class VerificacionRepository:
    def __init__(self):
        self.db_name = 'Verificador.db'

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table_verificaciones(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Verificaciones (
                    id_verificador INTEGER NOT NULL PRIMARY KEY,
                    id INTEGER,
                    fecha DATETIME NOT NULL,
                    verificador INTEGER NOT NULL,
                    usuario NVARCHAR(50),
                    tipo NVARCHAR(50),
                    categoria NVARCHAR(2)
                )
            ''')
            conn.commit()

    def create_verificacion(self, verificador=None, usuario=None, tipo=None, categoria=None):

        with self.connect_db() as conn:
            cursor = conn.cursor()

            # Obtener el siguiente id_verificador automaticamente
            cursor.execute('SELECT MAX(id_verificador) FROM Verificaciones')
            max_id = cursor.fetchone()[0]
            id_verificador = 1 if max_id is None else max_id + 1

            # Usar la fecha y hora actual
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insertar el nuevo registro
            cursor.execute('''
                INSERT INTO Verificaciones (id_verificador, id, fecha, verificador, usuario, tipo, categoria)
                VALUES (?, NULL, ?, ?, ?, ?, ?)
            ''', (id_verificador, fecha, verificador, usuario, tipo, categoria))
            conn.commit()

            return Verificacion(id_verificador, None, fecha, verificador, usuario, tipo, categoria)

    def get_all_verificaciones(self):
        """Obtener todas las verificaciones"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Verificaciones')
            registros = cursor.fetchall()

            verificaciones = []
            for registro in registros:
                verificacion = Verificacion(
                    id_verificador=registro[0],
                    id=registro[1],
                    fecha=registro[2],
                    verificador=registro[3],
                    usuario=registro[4],
                    tipo=registro[5],
                    categoria=registro[6]
                )
                verificaciones.append(verificacion)

        return verificaciones

    def get_verificaciones_sin_id(self):
        """Obtener verificaciones donde `id` es NULL"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Verificaciones WHERE id IS NULL')
            registros = cursor.fetchall()

            verificaciones = []
            for registro in registros:
                verificacion = Verificacion(
                    id_verificador=registro[0],
                    id=registro[1],
                    fecha=registro[2],
                    verificador=registro[3],
                    usuario=registro[4],
                    tipo=registro[5],
                    categoria=registro[6]
                )
                verificaciones.append(verificacion)

        return verificaciones

    def actualizar_id_verificacion(self, id_verificador, nuevo_id):
        """Actualizar el `id` de una verificacion"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Verificaciones
                SET id = ?
                WHERE id_verificador = ?
            ''', (nuevo_id, id_verificador))
            conn.commit()

    def get_verificaciones_por_usuario_y_fecha(self, usuario, fecha):
        """Obtener verificaciones por usuario y por fecha"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Verificaciones 
                WHERE usuario = ? AND fecha >= ? AND fecha < ?
            ''', (usuario, fecha + " 00:00:00", fecha + " 23:59:59"))
            registros = cursor.fetchall()

            verificaciones = []
            for registro in registros:
                verificacion = Verificacion(
                    id_verificador=registro[0],
                    id=registro[1],
                    fecha=registro[2],
                    verificador=registro[3],
                    usuario=registro[4],
                    tipo=registro[5],
                    categoria=registro[6]
                )
                verificaciones.append(verificacion)

        return verificaciones
