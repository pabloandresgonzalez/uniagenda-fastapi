from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Usuario
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: Optional[str] = "docente"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

# Espacio
class EspacioBase(BaseModel):
    nombre: str
    tipo: str
    capacidad: int
    ubicacion: str

class EspacioOut(EspacioBase):
    id: int
    class Config:
        orm_mode = True

# Evento
class EventoBase(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fecha_inicio: datetime
    fecha_fin: datetime

class EventoOut(EventoBase):
    id: int
    class Config:
        orm_mode = True

# Reserva
class ReservaBase(BaseModel):
    usuario_id: int
    espacio_id: int
    evento_id: int
    fecha_reserva: datetime
    observaciones: Optional[str]

class ReservaOut(ReservaBase):
    id: int
    estado: str
    class Config:
        orm_mode = True

# Login
class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: Optional[str] = "docente"

    class Config:
        orm_mode = True

class EspacioOut(BaseModel):
    id: int
    nombre: str
    tipo: str
    capacidad: int
    ubicacion: str

    class Config:
        orm_mode = True

class EventoOut(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    fecha_inicio: datetime
    fecha_fin: datetime

    class Config:
        orm_mode = True

class ReservaBase(BaseModel):
    usuario_id: int
    espacio_id: int
    evento_id: int
    fecha_reserva: datetime
    observaciones: Optional[str]

class ReservaOut(BaseModel):
    id: int
    usuario: Optional[UsuarioOut]  # Objeto anidado
    espacio: Optional[EspacioOut]
    evento: Optional[EventoOut]
    fecha_reserva: datetime
    observaciones: Optional[str]
    estado: str

    class Config:
        orm_mode = True
