from Repositorios.UsuarioRepository import UsuarioRepository
from Repositorios.VerificacionRepository import VerificacionRepository
from Datos import Datos
from Modulos.Solicitud import emitir_multiples_verificaciones
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from Modulos.Buzer import Buzer
from Modulos.Rgb import Rgb
from Modulos.Voz import Voz

class Autenticar:

    def __init__(self, parent):
        self.parent = parent
        self.root = parent
        self.buzer = Buzer()
        self.rgb = Rgb()
        self.voz = Voz()

    def autenticar_pin(self, pin):
        repositorio_usuario = UsuarioRepository()
        usuario = repositorio_usuario.get_usuario_by_pin(pin)
        self.autenticar(usuario, 'P')

    def autenticar_rfid(self, identificador):
        repositorio_usuario = UsuarioRepository()
        usuario = repositorio_usuario.get_usuario_by_rfid(identificador)
        self.autenticar(usuario, 'R')

    def autenticar_foto(self, foto):
        repositorio_usuario = UsuarioRepository()
        usuario = repositorio_usuario.get_usuario_by_foto(foto)
        self.autenticar(usuario, 'F')

    def autenticar_huella(self, huella):
        repositorio_usuario = UsuarioRepository()
        usuario = repositorio_usuario.get_usuario_by_huella(huella)
        self.autenticar(usuario, 'H')

    def autenticar(self, usuario, tipo):
        try:
            if usuario:
                datos = Datos.obtenerDatos()
                
                repositorio_verificacion = VerificacionRepository()
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                verificaciones = repositorio_verificacion.get_verificaciones_por_usuario_y_fecha(usuario.usuario, fecha_actual)
                
                # if verificaciones:
                    # ultima_verificacion = verificaciones[0]
                    # fecha_ultimo = ultima_verificacion.fecha  
                    # if isinstance(fecha_ultimo, str):
                        # fecha_ultimo = datetime.strptime(fecha_ultimo, '%Y-%m-%d %H:%M:%S')
                    
                    # if (fecha_actual - fecha_ultimo) < timedelta(minutes=10):
                        # print("Ya fue previamente autenticado")
                        # return
                        
                if datos:
                    repositorio_verificacion = VerificacionRepository()
                    verificacion = repositorio_verificacion.create_verificacion(
                        verificador=datos['identificador'],
                        usuario=usuario.usuario,
                        tipo=tipo,
                        categoria=self.obtener_categoria(usuario,verificaciones)
                    )
                    
                    if verificacion:
                        print(f"Usuario autenticado: {usuario.nombres}")
                        self.buzer.correcto()
                        self.rgb.set_color(False, True, False, 2)
                        self.voz.decir_mensaje("Bienvenido "+usuario.nombres)
                        emitir_multiples_verificaciones(datos['url'], [verificacion])
                    else:
                        print("Error el emitir la verificacion.")
                else:
                    print("No se encontraron datos para la verificacion.")
            else:
                print("Error: Usuario no identificado.")
                self.buzer.error()
                self.rgb.set_color(True, False, False, 2)
                self.voz.decir_mensaje("Usuario no identificado")
                
        except Exception as excepcion:
            print(f"Error inesperado: {excepcion}")
            self.buzer.error()
            self.rgb.set_color(True, False, False, 2)
        #finally:
         #   GPIO.cleanup()

    def obtener_categoria(self,usuario,verificaciones):
        if verificaciones:
            if len(verificaciones) == 1:
                return 'EI'
            elif len(verificaciones) == 2:
                return 'EF'
            else:
                return 'F'  
        else:
            return 'I'  
