import sqlite3

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Verificador.db')
cursor = conn.cursor()

class Turno:
    def __init__(self, id=None, nombre=None, descripcion=None, tolerancia=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tolerancia = tolerancia
        self.conn = sqlite3.connect('Verificador.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla Turnos si no existe
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre NVARCHAR(50),
                descripcion NVARCHAR(100),
                tolerancia INT
            )
        ''')
        self.conn.commit()

    def create_multiple_turnos(self, turnos_nuevos):
        """Borra todos los turnos existentes antes de agregar nuevos"""
        self.cursor.execute("DELETE FROM Turnos")
        self.conn.commit()
        
        # Insertar los nuevos turnos
        for turno in turnos_nuevos:
            self.cursor.execute(''' 
                INSERT INTO Turnos (nombre, descripcion, tolerancia)
                VALUES (?, ?, ?)
            ''', (turno.nombre, turno.descripcion, turno.tolerancia))
        self.conn.commit()
        print("Nuevos turnos creados correctamente.")

    def get_one_turno(self, turno_id):
        """Obtener un turno por ID"""
        self.cursor.execute('SELECT * FROM Turnos WHERE id = ?', (turno_id,))
        registro = self.cursor.fetchone()
        if registro:
            return Turno(id=registro[0], nombre=registro[1], descripcion=registro[2], tolerancia=registro[3])
        else:
            return None

def get_all_turnos():
        """Obtener todos los turnos"""
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
