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
