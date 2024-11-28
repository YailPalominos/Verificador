import threading
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time
from fastapi.encoders import jsonable_encoder
import base64
from Repositorios.TurnoRepositorio import TurnoRepositorio
from Repositorios.HorarioRepositorio import HorarioRepositorio
from Repositorios.UsuarioRepository import UsuarioRepository

class Horario(BaseModel):
    dia: str
    turno: int
    horarioInicio: time
    horarioFin: time
    entretiempoInicio: Optional[time] = None
    entretiempoFinal: Optional[time] = None

class Turno(BaseModel):
    id: int
    nombre: str
    descripcion: str
    tolerancia: Optional[int] = None

class UsuarioEmpleado(BaseModel):
    usuario: str
    nombres: str
    apellidos: str
    direccionCorreoElectronico: str
    turno: int
    pin: Optional[str] = None
    rfid: Optional[str] = None
    foto: Optional[str] = None
    huella: Optional[str] = None

class DatosVerificador(BaseModel):
    horarios: List[Horario]
    turnos: List[Turno]
    usuarios: List[UsuarioEmpleado]

class DatosVerificador(BaseModel):
    horarios: List[Horario]
    turnos: List[Turno]
    usuarios: List[UsuarioEmpleado]

app = FastAPI()
@app.post("/datos")
async def recibir_datos(datos: DatosVerificador):
    try:
        #Convercion a Json
        turnos_convertidos = jsonable_encoder(datos.turnos)
        horarios_convertidos=jsonable_encoder(datos.horarios)
        usuarios_convertidos=jsonable_encoder(datos.usuarios)
        #Actualizacion de propiedades
        horarios_transformados = transformar_horarios(horarios_convertidos)
        usuarios_transformados = transformar_usuarios(usuarios_convertidos) 
        #Creacion en los repositorios
        turnoRepositorio = TurnoRepositorio()
        horarioRepositorio = HorarioRepositorio()
        usuarioRepositorio = UsuarioRepository()
        turnoRepositorio.create_multiple_turnos(turnos_convertidos)
        horarioRepositorio.create_multiple_horarios(horarios_transformados)
        usuarioRepositorio.create_multiple_usuarios(usuarios_transformados)
        return {"mensaje": "Datos recibidos y actualizados correctamente"}
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return {"error": str(e)}


def transformar_horarios(json_entrante):
    horarios_transformados = []
    for item in json_entrante:
        horario_transformado = {
            'turno': item['turno'],
            'horario_inicio': item['horarioInicio'],
            'horario_fin': item['horarioFin'],
            'entretiempo_inicio': item.get('entretiempoInicio'),
            'entretiempo_final': item.get('entretiempoFinal'),
            'dia': item['dia']
        }
        horarios_transformados.append(horario_transformado)
    return horarios_transformados
    
def transformar_usuarios(json_entrante):
    usuarios_transformados = []
    for item in json_entrante:
        # Convertir foto y huella de Base64 a binario
        foto_binario = base64.b64decode(item['foto']) if 'foto' in item and item['foto'] else None
        huella_binario = base64.b64decode(item['huella']) if 'huella' in item and item['huella'] else None
        
        usuario_transformado = {
            'usuario': item['usuario'],
            'pin': item['pin'],
            'rfid': item['rfid'],
            'nombres': item['nombres'],
            'apellidos': item['apellidos'],
            'direccion_correo_electronico': item['direccionCorreoElectronico'],
            'huella': huella_binario,
            'foto': foto_binario,
            'turno': item['turno']
        }
        usuarios_transformados.append(usuario_transformado)
    return usuarios_transformados

# Convertir objetos de tipo 'time' en cadenas en formato 'HH:MM:SS'
def convert_time(obj):
    if isinstance(obj, time):
        return obj.strftime('%H:%M:%S')  # Convierte a formato HH:MM:SS
    raise TypeError("Type not serializable")


# Clase para manejar el servidor FastAPI
class Recepcion:
    def __init__(self):
        self.thread = threading.Thread(target=self.run_server, daemon=True)
        
    def start(self):
        """Inicia el hilo del servidor FastAPI"""
        print("Iniciando servidor FastAPI...")
        self.thread.start()

    def run_server(self):
        """Ejecuta el servidor FastAPI"""
        uvicorn.run(app, host="0.0.0.0", port=8000)
