import os

proyecto = {
    "database.py": '''\
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./uniagenda.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
''',

    "models.py": '''\
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
''',

    "schemas.py": '''\
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
''',

    "auth.py": '''\
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models
from database import SessionLocal

SECRET_KEY = "TU_SECRET_KEY_AQUI"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, correo: str, password: str):
    user = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if user is None:
        raise credentials_exception
    return user
''',

    "routers/__init__.py": "",

    "routers/usuarios.py": '''\
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=schemas.UsuarioOut)
def register(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == user.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    hashed_password = auth.get_password_hash(user.password)
    nuevo_usuario = models.Usuario(
        nombre=user.nombre,
        correo=user.correo,
        hashed_password=hashed_password,
        rol=user.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
''',

    "routers/espacios.py": '''\
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.EspacioOut])
def listar_espacios(db: Session = Depends(get_db)):
    return db.query(models.Espacio).all()

@router.post("/", response_model=schemas.EspacioOut)
def crear_espacio(espacio: schemas.EspacioBase, current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admins pueden crear espacios")
    nuevo = models.Espacio(**espacio.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
''',

    "routers/eventos.py": '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.EventoOut])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(models.Evento).all()

@router.post("/", response_model=schemas.EventoOut)
def crear_evento(evento: schemas.EventoBase, current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    nuevo = models.Evento(**evento.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
''',

    "routers/reservas.py": '''\
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.ReservaOut])
def listar_reservas(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()

@router.post("/", response_model=schemas.ReservaOut)
def crear_reserva(reserva: schemas.ReservaBase, current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    conflicto = db.query(models.Reserva).filter(
        models.Reserva.espacio_id == reserva.espacio_id,
        models.Reserva.estado == "confirmado",
        models.Reserva.fecha_reserva == reserva.fecha_reserva
    ).first()
    if conflicto:
        raise HTTPException(status_code=400, detail="Espacio ya reservado en esa fecha/hora")

    nueva_reserva = models.Reserva(**reserva.dict())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)

    print(f"Simulando envío de correo para reserva {nueva_reserva.id}")

    return nueva_reserva
''',

    "main.py": '''\
from fastapi import FastAPI
import models
from database import engine
from routers import usuarios, espacios, eventos, reservas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UniAgenda API")

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(espacios.router, prefix="/espacios", tags=["Espacios"])
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
'''
}

def crear_archivos():
    for ruta, contenido in proyecto.items():
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
    print("¡Proyecto UniAgenda creado con éxito!")

if __name__ == "__main__":
    crear_archivos()
