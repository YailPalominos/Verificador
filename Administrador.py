import tkinter as tk
from tkinter import ttk
from Datos import Datos
from Repositorios.UsuarioRepository import UsuarioRepository
from Repositorios.VerificacionRepository import VerificacionRepository
from Repositorios.HorarioRepositorio import HorarioRepositorio
from Repositorios.TurnoRepositorio import TurnoRepositorio
from Modulos.Solicitud import emitir_multiples_verificaciones
from Datos import Datos
from Modulos.EnvioNotificaciones import EnvioNotificaciones
from datetime import datetime

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

        self.crear_formulario_login()

        # Variable para las pestañas (inici     almente no se muestran)
        self.notebook = None


    def crear_formulario_login(self):
                """
                Crea y configura el formulario de login.
                """
                # Crear un marco para centrar los controles
                self.login_frame = tk.Frame(self.frame, bg="#222222")
                self.login_frame.pack(pady=100)

                self.usuario_label = tk.Label(self.login_frame, text="Usuario", font=("Arial", 18), bg="#222222", fg="white")
                self.usuario_label.grid(row=0, column=0, padx=10, pady=10)
                
                self.usuario_entry = tk.Entry(self.login_frame, font=("Arial", 18), bd=5, fg="white", bg="#444444", justify="center")
                self.usuario_entry.grid(row=0, column=1, padx=10, pady=10)

                self.contrasena_label = tk.Label(self.login_frame, text="Contraseña", font=("Arial", 18), bg="#222222", fg="white")
                self.contrasena_label.grid(row=1, column=0, padx=10, pady=10)

                self.contrasena_entry = tk.Entry(self.login_frame, font=("Arial", 18), bd=5, fg="white", bg="#444444", show=".  ", justify="center")
                self.contrasena_entry.grid(row=1, column=1, padx=10, pady=10)

                self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 18), command=self.login, bg="#5A6570", fg="white", bd=3)
                self.login_button.grid(row=2, column=0, columnspan=2, pady=20)
                
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
        #pestania5 = tk.Frame(self.notebook, bg="#222222")# Actualización huellas
        pestania6 = tk.Frame(self.notebook, bg="#222222")# Notificaciones

        # Agregar las pestañas al Notebook
        self.notebook.add(pestania1, text="Usuarios")
        self.notebook.add(pestania2, text="Verificaciones")
        self.notebook.add(pestania3, text="Turno")
        self.notebook.add(pestania4, text="Horario")
        #self.notebook.add(pestania5, text="Actualizar huellas")
        self.notebook.add(pestania6, text="Gestion")

        self.crear_tabla_usuarios(pestania1)
        self.crear_tabla_verificaciones(pestania2)
        self.crear_tabla_turnos(pestania3)
        self.crear_tabla_horarios(pestania4)
        self.crear_formulario_gestion(pestania6)
        
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
        repositorio_usuario = UsuarioRepository()
        usuarios = repositorio_usuario.get_all_usuarios()
        
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
            repositorio_horario = HorarioRepositorio()
            horarios = repositorio_horario.get_all_horarios()

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

        repositorio_turno = TurnoRepositorio()
        turnos = repositorio_turno.get_all_turnos()

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

        repositorio_verificacion = VerificacionRepository()
        verificaciones = repositorio_verificacion.get_all_verificaciones()

        # Insertar las verificaciones en la tabla
        for verificacion in verificaciones:
            tabla.insert("", "end", values=(verificacion.id_verificador, verificacion.fecha, verificacion.id, verificacion.usuario, verificacion.tipo, verificacion.categoria))

        # Usar after para esperar hasta que la ventana se haya renderizado antes de ajustar el tamaño de la tabla
        self.frame.after(100, self.ajustar_tabla, tabla, columnas)
        
        self.agregar_boton_actualizar(pestania)
        
        # Empacar la tabla dentro de la pestaña
        tabla.pack(padx=10, pady=10, fill="both", expand=True)

    def agregar_boton_actualizar(self, pestania):
            boton_actualizar = tk.Button(
                pestania,
                text="Actualizar",
                font=("Arial", 14),
                bg="#5A6570",
                fg="white",
                command=self.actualizar_verificaciones
            )
            boton_actualizar.pack(pady=20, side="bottom")
            
    def actualizar_verificaciones(self):
            repositorio_verificacion = VerificacionRepository()
            verificaciones = repositorio_verificacion.get_verificaciones_sin_id()
            datos = Datos.obtenerDatos()
            print(datos)
            if datos:  
                emitir_multiples_verificaciones(datos['url'], verificaciones)
                self.crear_tabla_verificaciones(self.notebook.tabs()[1])
            else:
                print("Datos no encontrados para la verificacion.")

    def crear_formulario_gestion(self, pestania):
            tk.Label(
                pestania,
                text="Propiedades de Datos:",
                font=("Arial", 16),
                bg="#222222",
                fg="white"
            ).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

            tk.Label(
                pestania,
                text="URL:",
                font=("Arial", 14),
                bg="#222222",
                fg="white"
            ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            url_entry = tk.Entry(pestania, font=("Arial", 14), width=40)
            url_entry.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(
                pestania,
                text="Identificador:",
                font=("Arial", 14),
                bg="#222222",
                fg="white"
            ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
            identificador_entry = tk.Entry(pestania, font=("Arial", 14), width=40)
            identificador_entry.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(
                pestania,
                text="Usuario:",
                font=("Arial", 14),
                bg="#222222",
                fg="white"
            ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
            usuario_entry = tk.Entry(pestania, font=("Arial", 14), width=40)
            usuario_entry.grid(row=2, column=1, padx=10, pady=10)

            tk.Label(
                pestania,
                text="Contrasena:",
                font=("Arial", 14),
                bg="#222222",
                fg="white"
            ).grid(row=3, column=0, padx=10, pady=10, sticky="w")
            contrasena_entry = tk.Entry(pestania, font=("Arial", 14), width=40, show="*")
            contrasena_entry.grid(row=3, column=1, padx=10, pady=10)

                # Botones
            tk.Button(
                    pestania,
                    text="Guardar Cambios",
                    font=("Arial", 14),
                    bg="#5A6570",
                    fg="white",
                    command=self.guardar_cambios 
            ).grid(row=6, column=0, columnspan=2, pady=20)

            tk.Button(
                    pestania,
                    text="Cerrar Sesion",
                    font=("Arial", 14),
                    bg="#A93226",
                    fg="white",
                    command=self.cerrar_sesion
            ).grid(row=5, column=1, padx=10, pady=10)

            tk.Button(
                    pestania,
                    text="Enviar Notificaciones",
                    font=("Arial", 14),
                    bg="#1E8449",
                    fg="white",
                    command=self.enviar_notificaciones 
            ).grid(row=5, column=0, padx=10, pady=10)


            datos = Datos.obtenerDatos()
            if datos:
                url_entry.insert(0, datos.get("url", ""))
                identificador_entry.insert(0, datos.get("identificador", ""))
                usuario_entry.insert(0, datos.get("usuario", ""))
                contrasena_entry.insert(0, datos.get("contrasena", ""))

    def enviar_notificaciones(self):
                repositorio_usuario = UsuarioRepository()
                usuarios = repositorio_usuario.get_all_usuarios()
                repositorio_verificacion = VerificacionRepository()
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
               
                for usuario in usuarios:
                    # Obtener verificaciones para el usuario y la fecha actual
                    verificaciones = repositorio_verificacion.get_verificaciones_por_usuario_y_fecha(usuario.usuario, fecha_actual)
                
                    # Imprimir las verificaciones encontradas para el usuario
                    if verificaciones:
                        EnvioNotificaciones.enviar_correo(usuario.direccion_correo_electronico,"Notificacion de verificaciones",usuario.nombres+" "+usuario.apellidos,verificaciones)
                        self.mostrar_mensaje("Notificaciones enviadas.", 2000, "blue")
                    else:
                        print(f"No se encontraron verificaciones para el usuario {usuario.nombres} el {fecha_actual}.")
                
        
    def cerrar_sesion(self):
            self.mostrar_mensaje("Sesion cerrada.", 2000, "blue")
            self.mostrar_login()

    def mostrar_login(self):
         for widget in self.parent.winfo_children():
           widget.destroy()
         self.crear_formulario_login()  


    def guardar_cambios(self):
            
            print("url_entry:", self.url_entry)
            nuevos_datos = {
                "url": url_entry.get(),
                "identificador": identificador_entry.get(),
                "usuario": usuario_entry.get(),
                "contrasena": contrasena_entry.get(),
            }

            if Datos.guardarDatos(nuevos_datos):
                self.mostrar_mensaje("Datos guardados correctamente.", 2000, "green")
            else:
                self.mostrar_mensaje("Error al guardar los datos.", 2000, "red")
