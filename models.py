from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="docente")
    reservas = relationship("Reserva", back_populates="usuario")

class Espacio(Base):
    __tablename__ = "espacios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    capacidad = Column(Integer)
    ubicacion = Column(String)
    reservas = relationship("Reserva", back_populates="espacio")

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    reservas = relationship("Reserva", back_populates="evento")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    espacio_id = Column(Integer, ForeignKey("espacios.id"))
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    estado = Column(String, default="confirmado")
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
    observaciones = Column(Text, nullable=True)

    usuario = relationship("Usuario", back_populates="reservas")
    espacio = relationship("Espacio", back_populates="reservas")
    evento = relationship("Evento", back_populates="reservas")
