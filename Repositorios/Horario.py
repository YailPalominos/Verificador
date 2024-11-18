import sqlite3

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Verificador.db')
cursor = conn.cursor()

class Horario:
    def __init__(self, turno=None, horario_inicio=None, horario_fin=None, entretiempo_inicio=None, entretiempo_final=None, dia=None):
        self.turno = turno
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.entretiempo_inicio = entretiempo_inicio
        self.entretiempo_final = entretiempo_final
        self.dia = dia
        self.conn = sqlite3.connect('Verificador.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla Horarios si no existe
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Horarios (
                turno INT NOT NULL,
                horario_inicio TIME(0) NOT NULL,
                horario_fin TIME(0) NOT NULL,
                entretiempo_inicio TIME(0),
                entretiempo_final TIME(0),
                dia NVARCHAR(10) NOT NULL,
                PRIMARY KEY (turno, dia)
            )
        ''')
        self.conn.commit()

    def create_multiple_horarios(self, horarios_nuevos):
        """Borra todos los horarios existentes antes de agregar nuevos"""
        self.cursor.execute("DELETE FROM Horarios")
        self.conn.commit()
        
        # Insertar los nuevos horarios
        for horario in horarios_nuevos:
            self.cursor.execute(''' 
                INSERT INTO Horarios (turno, horario_inicio, horario_fin, entretiempo_inicio, entretiempo_final, dia)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (horario.turno, horario.horario_inicio, horario.horario_fin, horario.entretiempo_inicio, horario.entretiempo_final, horario.dia))
        self.conn.commit()
        print("Nuevos horarios creados correctamente.")

    def get_all_by_turno(self, turno_id):
        """Obtener todos los horarios para un turno específico"""
        self.cursor.execute('SELECT * FROM Horarios WHERE turno = ?', (turno_id,))
        registros = self.cursor.fetchall()
        
        horarios = []
        for registro in registros:
            horario = Horario(
                turno=registro[0],
                horario_inicio=registro[1],
                horario_fin=registro[2],
                entretiempo_inicio=registro[3],
                entretiempo_final=registro[4],
                dia=registro[5]
            )
            horarios.append(horario)
        
        return horarios

def get_all_horarios():
        """Obtener todos los horarios"""
        cursor.execute('SELECT * FROM Horarios')
        registros = cursor.fetchall()
        
        horarios = []
        for registro in registros:
            horario = Horario(
                turno=registro[0],
                horario_inicio=registro[1],
                horario_fin=registro[2],
                entretiempo_inicio=registro[3],
                entretiempo_final=registro[4],
                dia=registro[5]
            )
            horarios.append(horario)
        
        return horarios
