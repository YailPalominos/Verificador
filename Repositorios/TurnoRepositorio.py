import sqlite3

class Turno:
    def __init__(self, id=None, nombre=None, descripcion=None, tolerancia=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tolerancia = tolerancia

    def __repr__(self):
        return (f"Turno(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion}, "
                f"tolerancia={self.tolerancia})")

class TurnoRepositorio:
    def __init__(self):
        self.db_name = 'Verificador.db'

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table_turnos(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Turnos (
                                id INTEGER PRIMARY KEY,
                                nombre NVARCHAR(50),
                                descripcion NVARCHAR(100),
                                tolerancia INT
                            )''')
            conn.commit()

    def get_all_turnos(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Turnos')
            registros = cursor.fetchall()

            turnos = []
            for registro in registros:
                turno = Turno(
                    id=registro[0],
                    nombre=registro[1],
                    descripcion=registro[2],
                    tolerancia=registro[3]
                )
                turnos.append(turno)

        return turnos

    def get_turno_by_id(self, turno_id):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Turnos WHERE id = ?', (turno_id,))
            registro = cursor.fetchone()

            if registro:
                return Turno(
                    id=registro[0],
                    nombre=registro[1],
                    descripcion=registro[2],
                    tolerancia=registro[3]
                )
            else:
                return None

    def create_multiple_turnos(self, turnos_nuevos):
            print(turnos_nuevos)
            """Borra todos los turnos existentes antes de agregar nuevos"""
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Turnos")
                conn.commit()

                for turno in turnos_nuevos:
                    cursor.execute('''
                        INSERT INTO Turnos (id, nombre, descripcion, tolerancia)
                        VALUES (?, ?, ?, ?)
                    ''', (turno['id'], turno['nombre'], turno['descripcion'], turno['tolerancia']))
                conn.commit()
                print("Nuevos turnos creados correctamente.")
