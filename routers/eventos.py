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

