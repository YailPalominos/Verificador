import sqlite3
from datetime import datetime

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Verificador.db')
cursor = conn.cursor()

# Crear tabla Verificaciones si no existe
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

# Modelo Verificacion
class Verificacion:
    def __init__(self, id_verificador, id, fecha, verificador, usuario, tipo, categoria):
        self.id_verificador = id_verificador
        self.id = id
        self.fecha = fecha
        self.verificador = verificador
        self.usuario = usuario
        self.tipo = tipo
        self.categoria = categoria  # Agregar el campo categoria

    def __repr__(self):
        return (f"Verificacion(id_verificador={self.id_verificador}, id={self.id}, "
                f"fecha={self.fecha}, verificador={self.verificador}, "
                f"usuario={self.usuario}, tipo={self.tipo}, categoria={self.categoria})")
        
def create_verificacion(verificador=None, usuario=None, tipo=None, categoria=None):
    try:
        # Obtener el siguiente id_verificador automáticamente
        cursor.execute('SELECT MAX(id_verificador) FROM Verificaciones')
        max_id = cursor.fetchone()[0]
        id_verificador = 1 if max_id is None else max_id + 1

        # Usar la fecha y hora actual
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insertar el nuevo registro en la tabla Verificaciones
        cursor.execute('''
            INSERT INTO Verificaciones (id_verificador, id, fecha, verificador, usuario, tipo, categoria)
            VALUES (?, NULL, ?, ?, ?, ?, ?)
        ''', (id_verificador, fecha, verificador, usuario, tipo, categoria))

        conn.commit()

        # Recuperar el registro insertado
        cursor.execute('''
            SELECT * FROM Verificaciones WHERE id_verificador = ?
        ''', (id_verificador,))
        registro = cursor.fetchone()

        if registro:
            return {
                "id_verificador": registro[0],
                "id": registro[1],
                "fecha": registro[2],
                "verificador": registro[3],
                "usuario": registro[4],
                "tipo": registro[5],
                "categoria": registro[6]
            }
        else:
            print("No se encontró el registro insertado.")
            return None

    except sqlite3.DatabaseError as e:
        conn.rollback()
        print(f"Error al insertar el registro: {e}")
        return None
    
def get_all_verificaciones():
    cursor.execute('SELECT * FROM Verificaciones')
    verificaciones_data = cursor.fetchall()
    
    # Convertir cada registro en una instancia de Verificacion y devolver en una lista
    verificaciones = [Verificacion(*fila) for fila in verificaciones_data]
    return verificaciones



# Función para actualizar el id de la verificación en la base de datos
def actualizar_id_verificacion(id_verificador, id):
    try:
        # Actualizar el id de la verificación en la base de datos
        cursor.execute('''
            UPDATE Verificaciones
            SET id = ?
            WHERE id_verificador = ?
        ''', (id, id_verificador))

        conn.commit()
        print(f"Verificación con id_verificador {id_verificador} actualizada con id {id}.")
    except sqlite3.DatabaseError as e:
        conn.rollback()
        print(f"Error al actualizar la verificación: {e}")


