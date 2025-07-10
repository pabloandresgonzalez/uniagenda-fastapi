from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import models
from database import engine
from routers import usuarios, espacios, eventos, reservas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UniAgenda API")

# Primero se define app, luego se usa:
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")

# Rutas
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(espacios.router, prefix="/espacios", tags=["Espacios"])
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])

application = app