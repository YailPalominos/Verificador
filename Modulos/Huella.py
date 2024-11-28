import serial
import time
import threading

# Configuracion de los pines
# VCC -> Pin 5V de la Raspberry Pi. (Rojo)
# TX -> Pin GPIO 14(Morado)
# RX -> Pin GPIO 15(Amarillo)
# GND -> Pin GND de la Raspberry Pi. (Blanco)

class Huella:
    def __init__(self):
        # Inicializacion de la clase Huella
        self.running = True  # Bandera para detener el hilo
        self.ser = None  # Inicializamos el puerto serial como None
        try:
            # Intentamos abrir el puerto serial
            self.ser = serial.Serial('/dev/ttyS0', 57600, timeout=1)
            print("Puerto serial abierto correctamente.")
        except Exception as e:
            print(f"Error al abrir el puerto serial: {e}")

        # Comandos del sensor
        self.START_CODE = 0x55
        self.CMD_ENROLL_START = 0x01
        self.CMD_ENROLL_NEXT = 0x02
        self.CMD_ENROLL_STOP = 0x03
        self.CMD_CAPTURE = 0x30
        print("Lectura de Huella iniciada")

    def iniciar(self):
        # Metodo que se ejecutara continuamente mientras la bandera `running` sea True
        while self.running:
            if self.ser and self.ser.is_open:  # Verificar si el puerto serial está disponible y abierto
                self.capture_fingerprint()
            else:
                print("No se pudo acceder al puerto serial.")
            time.sleep(1)  # Esperar un segundo entre cada intento

    # Funcion para calcular el checksum
    def checksum(self, data):
        return sum(data) & 0xFF

    # Funcion para enviar datos al sensor
    def send_data(self, command, data):
        if not self.ser or not self.ser.is_open:  # Verificar si el puerto serial esta disponible
            print("Puerto serial no esta disponible o no esta abierto.")
            return

        data_length = len(data)
        packet = [self.START_CODE, self.START_CODE, data_length + 2, command] + data
        checksum_value = self.checksum(packet)
        packet.append(checksum_value)
        self.ser.write(bytearray(packet))
        time.sleep(0.1)

    def capture_fingerprint(self):
        # Enviar comando para capturar la huella
        self.send_data(self.CMD_CAPTURE, [])
        response = self.ser.read(1024)  # Leer la respuesta del sensor
        
        print(response)
        # Verificar si la respuesta tiene la longitud esperada
        if len(response) < 9:
            return False

        # Verificar que la huella fue capturada correctamente
        if response[3] == 0x00:
            print("Huella capturada exitosamente")
            self.save_image(response[9:])  # Guardar la imagen si existe en la respuesta
            return True
        else:
            print(f"Error al capturar la huella. Codigo de error: {response[3]}")
            return False

    def save_image(self, image_data):
        # Guardar los datos de la imagen en un archivo
        filename = "huella_capturada.bmp"
        with open(filename, "wb") as img_file:
            img_file.write(image_data)
            print(f"Imagen de la huella guardada como {filename}")

    def stop(self):
        # Metodo para detener el hilo
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()  # Cerrar la conexion serial
