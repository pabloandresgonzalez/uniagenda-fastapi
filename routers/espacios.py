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

@router.put("/{id}", response_model=schemas.EspacioOut)
def actualizar_espacio(
    id: int,
    espacio_actualizado: schemas.EspacioBase,
    current_user=Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admins pueden actualizar espacios")

    espacio = db.query(models.Espacio).filter(models.Espacio.id == id).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")

    for key, value in espacio_actualizado.dict().items():
        setattr(espacio, key, value)

    db.commit()
    db.refresh(espacio)
    return espacio


