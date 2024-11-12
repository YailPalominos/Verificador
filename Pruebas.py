import sqlite3

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Verificador.db')
cursor = conn.cursor()

# Eliminar la tabla Verificaciones si ya existe
cursor.execute('DROP TABLE IF EXISTS Verificaciones')
conn.commit()

# Crear una nueva tabla Verificaciones con el campo 'categoria'
cursor.execute('''
    CREATE TABLE Verificaciones (
        id_verificador INTEGER NOT NULL PRIMARY KEY,
        id INTEGER,
        fecha DATETIME NOT NULL,
        verificador INTEGER NOT NULL,
        usuario NVARCHAR(50),
        tipo NVARCHAR(50),
        categoria NVARCHAR(2)  -- Añade el campo de categoria
    )
''')
conn.commit()

print("La tabla Verificaciones ha sido creada con el campo 'categoria'.")
