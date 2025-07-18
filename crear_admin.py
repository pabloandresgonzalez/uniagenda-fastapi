from database import SessionLocal
import models
import auth

def crear_usuario_admin():
    db = SessionLocal()
    correo = "admin@uniagenda.com"  # Cambia por el correo que quieras
    nombre = "Administrador"
    rol = "admin"
    password = "admin123"  # Cambia la contraseña segura

    # Verificar si ya existe usuario con ese correo
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if usuario_existente:
        print(f"El usuario con correo {correo} ya existe.")
        return

    hashed_password = auth.get_password_hash(password)
    nuevo_usuario = models.Usuario(
        nombre=nombre,
        correo=correo,
        hashed_password=hashed_password,
        rol=rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    print(f"Usuario admin creado:\nCorreo: {correo}\nContraseña: {password}")

    db.close()

if __name__ == "__main__":
    crear_usuario_admin()
