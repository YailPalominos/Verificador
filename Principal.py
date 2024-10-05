import tkinter as tk
import time
import subprocess  # Para ejecutar otro script de Python
import Voz

# Función para actualizar la hora
def actualizar_reloj():
    hora_actual = time.strftime('%H:%M:%S')
    reloj.config(text=hora_actual)
    panel.after(1000, actualizar_reloj)

# Función para manejar la acción de los botones numéricos
def boton_click(numero):
    texto_numeros.set(texto_numeros.get() + str(numero))  # Agrega el número presionado

# Función para borrar el último carácter escrito
def boton_borrar_ultimo():
    texto_actual = texto_numeros.get()
    texto_numeros.set(texto_actual[:-1])  # Elimina el último carácter

# Función para borrar todo lo escrito
def boton_borrar_todo():
    texto_numeros.set("")  # Limpia todo el contenido del campo de texto

# Función para manejar el botón "Enter"
def boton_enter():
    pin_ingresado = texto_numeros.get()
    print(f"Valor ingresado: {pin_ingresado}")  # Acción al presionar Enter
    if pin_ingresado == "123456":  # Comprobación del PIN
        subprocess.run(["python", "Voz.py"])  # Ejecuta el script Voz.py
    texto_numeros.set("")  # Limpia el campo después de presionar Enter

# Función para manejar el botón "Modo"
def boton_modo():
    print("Modo activado")  # Acción al presionar Modo

# Crear una instancia de la aplicación
root = tk.Tk()

# Configurar la ventana para que se abra en pantalla completa
root.attributes('-fullscreen', True)

# Salir del modo pantalla completa con 'Esc'
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Crear un Frame que será el panel principal con fondo claro
panel = tk.Frame(root, bg="#222222")  # Color de fondo más claro
panel.pack(fill="both", expand=True)

# Crear el reloj en la parte superior
reloj = tk.Label(panel, font=("Arial", 48), fg="white", bg="#222222")  # Color de fondo del reloj
reloj.pack(pady=10)

# Iniciar la actualización del reloj
actualizar_reloj()

# Variable para mostrar el texto de los números presionados
texto_numeros = tk.StringVar()
texto_numeros.set("")

# Etiqueta para ingresar el PIN
etiqueta_pin = tk.Label(panel, text="Ingrese el PIN", font=("Arial", 24), fg="white", bg="#222222")  # Color de fondo
etiqueta_pin.pack(pady=10)

# Crear un Entry para mostrar los números ingresados con estilo en negritas
display = tk.Entry(panel, textvariable=texto_numeros, font=("Arial", 36, "bold"), 
                   fg="white", bg="#222222", justify='right', bd=5)
display.pack(pady=10, padx=20)  # Ajuste del ancho del Entry

# Configurar el tamaño del Entry con un ancho fijo
display.config(width=10)  # Ancho fijo del Entry

# Crear un Frame para el tablero numérico de 0 a 9 y el botón Enter
tablero = tk.Frame(panel, bg="#222222")  # Sin fondo gris
tablero.pack(pady=10, padx=10)

# Crear los botones numéricos con fondo claro
botones = []
for i in range(1, 10):  # Botones del 1 al 9
    boton = tk.Button(tablero, text=str(i), font=("Arial", 24), width=5, height=2, 
                      command=lambda i=i: boton_click(i), fg="black", bg="lightgray", bd=3)
    botones.append(boton)

# Colocar los botones en la cuadrícula (3x3 para los números 1-9)
for idx, boton in enumerate(botones):
    fila = idx // 3
    columna = idx % 3
    boton.grid(row=fila, column=columna, padx=5, pady=5)

# Botón "0" debajo del "1"
boton_cero = tk.Button(tablero, text="0", font=("Arial", 24), width=5, height=2, 
                       command=lambda: boton_click(0), fg="black", bg="lightgray", bd=3)
boton_cero.grid(row=3, column=0, padx=5, pady=5)

# Botón "Confirmar" que ocupa dos columnas (donde están "2" y "3")
boton_confirmar = tk.Button(tablero, text="Confirmar", font=("Arial", 24), width=12, height=2, 
                             command=boton_enter, fg="black", bg="lightgray", bd=3)
boton_confirmar.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

# Botón para borrar el último carácter escrito
boton_borrar_ultimo = tk.Button(tablero, text="⌫", font=("Arial", 24), width=5, height=2, 
                                command=boton_borrar_ultimo, fg="black", bg="lightgray", bd=3)
boton_borrar_ultimo.grid(row=0, column=3, padx=5, pady=5)

# Botón para borrar todo el contenido (reemplazado por "X")
boton_borrar_todo = tk.Button(tablero, text="X", font=("Arial", 24), width=5, height=2, 
                              command=boton_borrar_todo, fg="black", bg="lightgray", bd=3)
boton_borrar_todo.grid(row=1, column=3, padx=5, pady=5)

# Botón "Modo" que ocupa desde el botón "3" hasta el botón "Confirmar"
boton_modo = tk.Button(tablero, text="Modo", font=("Arial", 24), width=12, height=4, 
                       command=boton_modo, fg="black", bg="lightgray", bd=3)
boton_modo.grid(row=2, column=3, rowspan=2, padx=5, pady=5)  # Ocupa dos filas hacia abajo

# Iniciar el bucle de la aplicación
root.mainloop()
