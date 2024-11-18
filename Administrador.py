import tkinter as tk
from tkinter import ttk
from Datos import Datos
from Usuario import get_all_usuarios
from Verificacion import get_all_verificaciones
from Repositorios.Horario import get_all_horarios
from Turno import get_all_turnos

class Administrador:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="#222222")
        self.frame.pack(fill="both", expand=True)

        # Cargar las credenciales desde el archivo JSON
        self.datos = Datos.obtenerDatos("Datos.json")
        
        if not self.datos:
            print("Error: No se pudo cargar los datos.")
            return
        
        self.usuario_correcto = self.datos['usuario']
        self.contrasena_correcta = self.datos['contrasena']

        # Crear un marco para centrar los controles
        self.login_frame = tk.Frame(self.frame, bg="#222222")
        self.login_frame.pack(pady=100)

        # Etiqueta y campo de entrada para el usuario
        self.usuario_label = tk.Label(self.login_frame, text="Usuario", font=("Arial", 18), bg="#222222", fg="white")
        self.usuario_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.usuario_entry = tk.Entry(self.login_frame, font=("Arial", 18), bd=5, fg="white", bg="#444444", justify="center")
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta y campo de entrada para la contraseña
        self.contrasena_label = tk.Label(self.login_frame, text="Contraseña", font=("Arial", 18), bg="#222222", fg="white")
        self.contrasena_label.grid(row=1, column=0, padx=10, pady=10)

        self.contrasena_entry = tk.Entry(self.login_frame, font=("Arial", 18), bd=5, fg="white", bg="#444444", show="•", justify="center")
        self.contrasena_entry.grid(row=1, column=1, padx=10, pady=10)

        # Botón de Login
        self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 18), command=self.login, bg="#5A6570", fg="white", bd=3)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Variable para las pestañas (inicialmente no se muestran)
        self.notebook = None

    def login(self):
        """
        Función para manejar el login, comparando las credenciales ingresadas con las del JSON.
        """
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        # Validar las credenciales
        if usuario == self.usuario_correcto and contrasena == self.contrasena_correcta:
            print("Login exitoso.")
            # Deshabilitar la pantalla de login
            self.login_frame.pack_forget()

            # Crear y mostrar las pestañas después del login exitoso
            self.crear_pestanas()

            # Mostrar el mensaje flotante de éxito sin modificar el canvas
            self.mostrar_mensaje("Login exitoso.", 2000,"green")
        else:
            print("Login fallido.")
            # Limpiar campos de login
            self.usuario_entry.delete(0, tk.END)
            self.contrasena_entry.delete(0, tk.END)
            self.usuario_entry.focus()
            self.mostrar_mensaje("Credenciales incorrectas.", 2000,"red")

    def mostrar_mensaje(self, mensaje, duracion,color):
        """
        Muestra un mensaje flotante en la pantalla por una duración especificada
        sin alterar el tamaño del canvas.
        """
        mensaje_label = tk.Label(self.frame, text=mensaje, font=("Arial", 16), bg=color, fg="white", padx=10, pady=5)
        mensaje_label.place(x=300, y=50)

        # Después de la duración, eliminar el mensaje flotante
        self.frame.after(duracion, mensaje_label.destroy)

    def crear_pestanas(self):
        """
        Crear y mostrar las pestañas dentro de la clase Administrador.
        """
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)

        # Crear las pestañas
        pestania1 = tk.Frame(self.notebook, bg="#222222")# Usuarios
        pestania2 = tk.Frame(self.notebook, bg="#222222")# Verificaciones
        pestania3 = tk.Frame(self.notebook, bg="#222222")# Turno
        pestania4 = tk.Frame(self.notebook, bg="#222222")# Horario
        pestania5 = tk.Frame(self.notebook, bg="#222222")# Actualización información
        pestania6 = tk.Frame(self.notebook, bg="#222222")# Verificación Rfid

        # Agregar las pestañas al Notebook
        self.notebook.add(pestania1, text="Usuarios")
        self.notebook.add(pestania2, text="Verificaciones")
        self.notebook.add(pestania3, text="Turno")
        self.notebook.add(pestania4, text="Horario")
        self.notebook.add(pestania5, text="Actualizar")
        self.notebook.add(pestania6, text="Verificar Rfid")

        # Agregar contenido a la primera pestaña (Tabla de usuarios)
        self.crear_tabla_usuarios(pestania1)
        
        # Agregar contenido a la segunda pestaña (Tabla de verificaciones)
        self.crear_tabla_verificaciones(pestania2)
        
        # Agregar contenido a la segunda pestaña (Tabla de verificaciones)
        self.crear_tabla_turnos(pestania3)
        
        # Agregar contenido a la segunda pestaña (Tabla de verificaciones)
        self.crear_tabla_horarios(pestania4)
        
        

    def crear_tabla_usuarios(self, pestania):
        """
        Crear una tabla simple en la pestaña de usuarios con las nuevas propiedades.
        """
        # Crear un árbol para la tabla
        columnas = ("Usuario", "Pin", "RFID", "Nombres", "Apellidos", "Correo Electrónico", "Turno", "Huella", "Foto")
        tabla = ttk.Treeview(pestania, columns=columnas, show="headings")

        # Definir encabezados de la tabla
        for col in columnas:
            tabla.heading(col, text=col)

        # Obtener los usuarios de la base de datos
        usuarios = get_all_usuarios()
        print(usuarios)

        # Insertar los usuarios en la tabla
        for usuario in usuarios:
            # Asumimos que "turno" es un número, "huella" y "foto" se mantienen como BLOBs (o se procesan según sea necesario)
            tabla.insert("", "end", values=(
                usuario.usuario, 
                usuario.pin, 
                usuario.rfid, 
                usuario.nombres, 
                usuario.apellidos, 
                usuario.direccion_correo_electronico, 
                usuario.turno, 
                "Disponible" if usuario.huella else "No disponible",  # Ejemplo de procesamiento para mostrar huella
                "Disponible" if usuario.foto else "No disponible"      # Ejemplo de procesamiento para mostrar foto
            ))

        # Usar after para esperar hasta que la ventana se haya renderizado antes de ajustar el tamaño de la tabla
        self.frame.after(100, self.ajustar_tabla, tabla, columnas)


    def crear_tabla_horarios(self, pestania):
            """
            Crear una tabla de horarios en la interfaz de usuario.
            """
            # Crear un árbol para la tabla
            columnas = ("Turno", "Horario Inicio", "Horario Fin", "Entretiempo Inicio", "Entretiempo Final", "Día")
            tabla = ttk.Treeview(pestania, columns=columnas, show="headings")

            # Definir encabezados de la tabla
            for col in columnas:
                tabla.heading(col, text=col)

            # Obtener los horarios de la base de datos
            horarios = get_all_horarios()
            print(horarios)

            # Insertar los horarios en la tabla
            for h in horarios:
                tabla.insert("", "end", values=(h.turno, h.horario_inicio, h.horario_fin, h.entretiempo_inicio, h.entretiempo_final, h.dia))

            # Usar after para esperar hasta que la ventana se haya renderizado antes de ajustar el tamaño de la tabla
            self.frame.after(100, self.ajustar_tabla, tabla, columnas)


    def crear_tabla_turnos(self, pestania):
        """
        Crear una tabla de turnos en la interfaz de usuario.
        """
        # Crear un árbol para la tabla
        columnas = ("ID", "Nombre", "Descripción", "Tolerancia")
        tabla = ttk.Treeview(pestania, columns=columnas, show="headings")

        # Definir encabezados de la tabla
        for col in columnas:
            tabla.heading(col, text=col)

        # Obtener los turnos de la base de datos
        turnos = get_all_turnos()
        print(turnos)

        # Insertar los turnos en la tabla
        for t in turnos:
            tabla.insert("", "end", values=(t.id, t.nombre, t.descripcion, t.tolerancia))

        # Usar after para esperar hasta que la ventana se haya renderizado antes de ajustar el tamaño de la tabla
        self.frame.after(100, self.ajustar_tabla, tabla, columnas)

    def ajustar_tabla(self, tabla, columnas):
        """
        Ajusta el tamaño de las columnas de la tabla después de que la ventana se haya renderizado.
        """
        # Obtener el ancho de la ventana y calcular el tamaño de las columnas
        tabla_width = self.frame.winfo_width() * 0.8  # 80% del ancho de la ventana
        column_width = int(tabla_width / len(columnas))  # Redondear a entero

        for col in columnas:
            tabla.column(col, width=column_width, anchor="center")

        # Centrar la tabla
        tabla.place(relx=0.5, rely=0.5, anchor="center")

        # Empacar la tabla dentro de la pestaña
        tabla.pack(padx=10, pady=10, fill="both", expand=True)
        
        
        
    def crear_tabla_verificaciones(self, pestania):
        """
        Crear una tabla simple en la pestaña de verificaciones.
        """
        # Crear un árbol para la tabla
        columnas = ("ID Verificador", "Fecha", "Id", "Usuario", "Tipo", "Categoria")
        tabla = ttk.Treeview(pestania, columns=columnas, show="headings")

        # Definir encabezados de la tabla
        for col in columnas:
            tabla.heading(col, text=col)

        # Obtener las verificaciones de la base de datos
        verificaciones = get_all_verificaciones()

        # Insertar las verificaciones en la tabla
        for verificacion in verificaciones:
            tabla.insert("", "end", values=(verificacion.id_verificador, verificacion.fecha, verificacion.id, verificacion.usuario, verificacion.tipo, verificacion.categoria))

        # Usar after para esperar hasta que la ventana se haya renderizado antes de ajustar el tamaño de la tabla
        self.frame.after(100, self.ajustar_tabla, tabla, columnas)
