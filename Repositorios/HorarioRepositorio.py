import sqlite3

class Horario:
    def __init__(self, turno=None, horario_inicio=None, horario_fin=None, entretiempo_inicio=None, entretiempo_final=None, dia=None):
        self.turno = turno
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.entretiempo_inicio = entretiempo_inicio
        self.entretiempo_final = entretiempo_final
        self.dia = dia

    def __repr__(self):
        return (f"Horario(turno={self.turno}, horario_inicio={self.horario_inicio}, "
                f"horario_fin={self.horario_fin}, entretiempo_inicio={self.entretiempo_inicio}, "
                f"entretiempo_final={self.entretiempo_final}, dia={self.dia})")


class HorarioRepositorio:
    def __init__(self):
        self.db_name = 'Verificador.db'

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table_horarios(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
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
            conn.commit()

    def create_multiple_horarios(self, horarios_nuevos):
        """Borra todos los horarios existentes antes de agregar nuevos"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Horarios")
            conn.commit()

            # Insertar los nuevos horarios
            for horario in horarios_nuevos:
                cursor.execute(''' 
                    INSERT INTO Horarios (turno, horario_inicio, horario_fin, entretiempo_inicio, entretiempo_final, dia)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (horario['turno'], horario['horario_inicio'], horario['horario_fin'], horario['entretiempo_inicio'], horario['entretiempo_final'], horario['dia']))
            conn.commit()
            print("Nuevos horarios creados correctamente.")

    def get_all_by_turno(self, turno_id):
        """Obtener todos los horarios para un turno especifico"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Horarios WHERE turno = ?', (turno_id,))
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

    def get_all_horarios(self):
        """Obtener todos los horarios"""
        with self.connect_db() as conn:
            cursor = conn.cursor()
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
