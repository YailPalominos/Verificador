
import sqlite3

class ReiniciarTablas:
    def __init__(self, db_name='Verificador.db'):
        self.db_name = db_name

    def connect_db(self):
        """Conecta con la base de datos."""
        return sqlite3.connect(self.db_name)

    def reiniciar_tablas(self):
        """Elimina los datos de todas las tablas sin eliminar las estructuras."""
        with self.connect_db() as conn:
            cursor = conn.cursor()

            # Obtener nombres de todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tablas = cursor.fetchall()

            if not tablas:
                print("No hay tablas para reiniciar.")
                return

            # Eliminar los datos de cada tabla
            for (tabla,) in tablas:
                cursor.execute(f"DELETE FROM {tabla};")
                print(f"Datos eliminados en la tabla: {tabla}")

            conn.commit()
            print("Reinicio de datos en tablas completado.")

# Uso del script
if __name__ == "__main__":
    reiniciar = ReiniciarTablas()
    reiniciar.reiniciar_tablas()
