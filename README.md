# 📅 UniAgenda - Sistema de Reservas Universitarias

**UniAgenda** es una API RESTful desarrollada con **FastAPI** que permite a instituciones universitarias gestionar la reserva de espacios como aulas, auditorios, laboratorios y más. Incluye autenticación, notificaciones automáticas, historial y gestión de usuarios.


---

## 🚀 Tecnologías Usadas

- **FastAPI** (v0.110.0)
- **SQLAlchemy** (ORM)
- **JWT** (Autenticación con `python-jose`)
- **Uvicorn** (servidor ASGI)
- **MySQL** (base de datos)
- **Jinja2** (plantillas HTML)
- **FullCalendar.js** (interfaz de calendario)
- **JavaScript + HTML** (interfaz simple de usuario)

---

## ⚙️ Instalación local

```bash
# Clona el repositorio
git clone https://github.com/pabloandresgonzalez/uniagenda-fastapi.git
cd uniagenda-fastapi

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta el servidor
uvicorn main:app --reload
```

Abre en tu navegador: [http://127.0.0.1:8000/static/calendario.html](http://127.0.0.1:8000/static/calendario.html)

---

## 📁 Estructura del Proyecto

```
uniagenda-fastapi/
├── main.py               # Entrada principal de la app
├── database.py           # Configuración de SQLAlchemy
├── models/               # Modelos de base de datos
├── routers/              # Rutas (usuarios, eventos, espacios, reservas)
├── schemas/              # Validaciones Pydantic
├── static/               # Archivos estáticos (calendario, JS, CSS)
├── templates/            # Plantillas HTML
├── requirements.txt      # Dependencias
└── README.md             # Este archivo
```

---

## 🔐 Autenticación

- Autenticación basada en tokens JWT
- Registro y login de usuarios
- Seguridad para rutas protegidas

---

## 🔄 Funcionalidades

- Registro y autenticación de usuarios
- CRUD de espacios universitarios
- Gestión de reservas
- Calendario interactivo
- Interfaz básica en HTML + JS
- Validaciones automáticas con Pydantic
- Notificaciones configurables (correo o áreas TI, audiovisuales, etc.)

---

## 📆 Calendario de Reservas

Se utiliza **FullCalendar.js** para mostrar visualmente los eventos reservados.

---

## 📌 Próximas mejoras

- Roles de usuario (admin, docente, estudiante)
- Envío automático de correos
- Panel de administración
- Validaciones de conflictos de horarios
- Responsivo para móviles

---

## 👨‍💻 Autor

**Pablo Andrés González**  
📧 [pabloandresgonzalez@correo.com]  
🔗 [github.com/pabloandresgonzalez](https://github.com/pabloandresgonzalez)

---

## 📝 Licencia

Este proyecto se distribuye bajo la licencia MIT.