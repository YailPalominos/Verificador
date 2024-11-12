import tkinter as tk
import time
from Usuario import get_usuario_by_pin
from Verificacion import create_verificacion
from Datos import Datos
from Solicitud import emitir_multiples_verificaciones
from tkinter import ttk
from Voz import Voz
class Pin:
    
    def __init__(self, parent):
        self.parent = parent
        self.texto_numeros = tk.StringVar()
        self.texto_numeros.set("")

    # Función para actualizar la hora
    def actualizar_reloj(self):
        hora_actual = time.strftime('%H:%M:%S')
        self.reloj.config(text=hora_actual)
        self.reloj.after(1000, self.actualizar_reloj)  # Actualiza cada segundo

    # Función para manejar la acción de los botones numéricos
    def boton_click(self, numero):
        self.texto_numeros.set(self.texto_numeros.get() + str(numero))

    # Función para borrar el último carácter escrito
    def boton_borrar_ultimo(self):
        texto_actual = self.texto_numeros.get()
        self.texto_numeros.set(texto_actual[:-1])

    def boton_enter(self):
        pin_ingresado = self.texto_numeros.get()
        print(f"Pin ingresado: {pin_ingresado}")

        # Obtener usuario por PIN
        usuario = get_usuario_by_pin(pin_ingresado)
        
        if usuario:
            # Obtener los datos usando el método de la clase Datos
            datos = Datos.obtenerDatos()  # Asumiendo que esto retorna un diccionario con 'identificador', 'url', etc.
            if datos:
                # Crear verificación pasando los datos y el usuario encontrado
                verificacion = create_verificacion(verificador=datos['identificador'], 
                                                usuario=usuario.usuario, tipo='P',categoria='I')
                # Verificar si la creación fue exitosa
                if verificacion is not None:
                    voz = Voz()  # Crear instancia de Voz
                    voz.decir_mensaje("Bienvenido, "+usuario.nombres)
                    print("Verificación creada exitosamente:", verificacion)
                    emitir_multiples_verificaciones(datos['url'],[verificacion])
                else:
                    print("Error: La verificación no se pudo crear.")
            else:
                print("Datos no encontrados para la verificación.")
        else:
            print("Usuario no identificado")
        
        self.texto_numeros.set("")

    def crear_interfaz(self):
        # Crear panel para el reloj y display del PIN
        self.panel = tk.Frame(self.parent, bg="#222222")
        self.panel.pack(fill="both", expand=True)

        # Crear el reloj en la parte superior
        self.reloj = tk.Label(self.panel, font=("Arial", 32), fg="white", bg="#222222")
        self.reloj.pack(pady=5)
        self.actualizar_reloj()  # Inicia la actualización del reloj superior

        # Etiqueta para ingresar el PIN
        etiqueta_pin = tk.Label(self.panel, text="Ingrese el PIN", font=("Arial", 18), fg="white", bg="#222222")
        etiqueta_pin.pack(pady=5)

        # Display para el PIN
        display = tk.Entry(self.panel, textvariable=self.texto_numeros, font=("Arial", 28, "bold"),
                        fg="white", bg="#222222", justify='right', bd=5, show="•")
        display.pack(pady=5, padx=15)
        display.config(width=8)

        # Crear el tablero numérico de 0 a 9 y el botón Enter
        tablero = tk.Frame(self.panel, bg="#222222")
        tablero.pack(pady=5, padx=5)

        # Crear los botones numéricos con tamaño más pequeño
        botones = []
        for i in range(1, 10):
            boton = tk.Button(tablero, text=str(i), font=("Arial", 18), width=4, height=1,
                            command=lambda i=i: self.boton_click(i), fg="black", bg="lightgray", bd=3)
            botones.append(boton)

        # Colocar los botones en la cuadrícula (3x3 para los números 1-9)
        for idx, boton in enumerate(botones):
            fila = idx // 3
            columna = idx % 3
            boton.grid(row=fila, column=columna, padx=3, pady=3)

        # Botón "0"
        boton_cero = tk.Button(tablero, text="0", font=("Arial", 18), width=4, height=1,
                            command=lambda: self.boton_click(0), fg="black", bg="lightgray", bd=3)
        boton_cero.grid(row=3, column=1, padx=3, pady=3)

        # Botón "Confirmar"
        boton_confirmar = tk.Button(tablero, text="✓", font=("Arial", 18), width=4, height=1,
                                    command=self.boton_enter, fg="white", bg="#7D8B8C", bd=3)
        boton_confirmar.grid(row=3, column=2, padx=3, pady=3)

        # Botón para borrar el último carácter escrito
        boton_borrar_ultimo = tk.Button(tablero, text="<", font=("Arial", 18), width=4, height=1,
                                        command=self.boton_borrar_ultimo, fg="white", bg="#5A6570", bd=3)
        boton_borrar_ultimo.grid(row=3, column=0, padx=3, pady=3)