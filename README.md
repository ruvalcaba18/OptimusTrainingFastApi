# Optimus Training API 🏋️

API de deportes y entrenamiento construida con **FastAPI**, diseñada para escalar a **100 mil usuarios**. Sigue una arquitectura de capas clara: Routes → Controllers → Services → Database → Models.

---

## ✨ Características

- **Arquitectura de capas** — Routes, Controllers, Services, Database, Models con separación total de responsabilidades.
- **Versionado de API** — Toda la API vive bajo `/api/v1/`. Agregar `v2` no rompe nada.
- **Foto de perfil** — Endpoint dedicado para subir imagen JPG/PNG/WEBP (máx 5 MB) por usuario.
- **Archivos estáticos** — Las fotos se sirven en `/uploads/profile_pictures/` vía HTTP.
- **Pool de conexiones** — Configurado para alta concurrencia (`pool_size=10`, `max_overflow=20`).
- **Autenticación JWT** — Tokens Bearer con expiración configurable.
- **Validación estricta** — Pydantic v2 (email, teléfono regex, enum de tipo de entrenamiento).
- **Schemas comunes reutilizables** — `PaginatedResponse[T]` genérico y `MessageResponse`.
- **Tests con SQLite en memoria** — 15 tests, sin necesitar PostgreSQL en CI.
- **Documentación automática** — Swagger UI y ReDoc integrados.

---

## 🛠️ Stack tecnológico

| Librería | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web principal |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM + gestión de conexiones |
| [PostgreSQL](https://www.postgresql.org/) | Base de datos en producción |
| [Pydantic v2](https://docs.pydantic.dev/) | Validación y serialización |
| [Python-JOSE](https://python-jose.readthedocs.io/) | Generación y verificación de JWT |
| [Passlib + bcrypt](https://passlib.readthedocs.io/) | Hash seguro de contraseñas |
| [python-multipart](https://andrew-d.github.io/python-multipart/) | Soporte de uploads de archivos |
| [pytest + httpx](https://docs.pytest.org/) | Suite de tests |

---

## 📁 Estructura del proyecto

```
OptimusTrainingFastApi/
│
├── app/
│   ├── api/
│   │   ├── deps.py                       # Dependencias reutilizables (get_current_user)
│   │   └── v1/
│   │       ├── router.py                 # Agrega todos los routers de v1
│   │       └── routes/                   # ← CAPA 1: solo declaran endpoints HTTP
│   │           ├── auth.py
│   │           └── users.py              # incluye POST /{id}/photo
│   │
│   ├── controllers/                      # ← CAPA 2: lógica HTTP + autorización
│   │   ├── __init__.py                   # re-exporta todos los controllers
│   │   ├── auth/
│   │   │   └── auth_controller.py
│   │   └── users/
│   │       └── user_controller.py
│   │
│   ├── services/                         # ← CAPA 3: lógica de negocio pura
│   │   ├── user_service.py
│   │   └── upload_service.py             # Validación y guardado de fotos
│   │
│   ├── database/                         # ← CAPA 4: configuración de DB
│   │   ├── __init__.py                   # re-exporta Base, get_db, engine
│   │   └── session/
│   │       └── session.py               # Engine + pool + SessionLocal + Base
│   │
│   ├── models/                           # ← CAPA 5: modelos SQLAlchemy
│   │   └── user.py                       # + profile_picture_url, is_active, timestamps
│   │
│   ├── schemas/                          # Pydantic — dividido por dominio
│   │   ├── users/                        # Schemas del dominio usuarios
│   │   │   ├── user_base.py
│   │   │   ├── user_create.py
│   │   │   ├── user_update.py
│   │   │   ├── user_response.py          # + profile_picture_url, created_at
│   │   │   ├── user_login.py
│   │   │   ├── token.py
│   │   │   └── training_type.py          # Enum: casa | afuera | gimnasio | mixto
│   │   ├── sports/                       # Schemas del dominio deportes (listo para crecer)
│   │   └── common/                       # Schemas reutilizables entre dominios
│   │       ├── pagination.py             # PaginatedResponse[T] genérico
│   │       └── response.py              # MessageResponse
│   │
│   ├── core/                             # Configuración global
│   │   ├── config.py                     # Settings con pydantic-settings + .env
│   │   ├── security.py                   # JWT + bcrypt helpers
│   │   ├── middleware.py                 # AuthMiddleware + X-Process-Time
│   │   └── db.py                         # Shim de compatibilidad → database/session
│   │
│   ├── uploads/
│   │   └── profile_pictures/             # Fotos de perfil (servidas en /uploads/...)
│   │       └── .gitkeep                  # Mantiene el folder en git aunque esté vacío
│   │
│   └── main.py                           # Entry point: app, middlewares, rutas, uploads
│
├── tests/
│   ├── conftest.py                       # Fixtures: client, db, test_user, auth_headers
│   ├── test_auth.py                      # Tests de login
│   └── test_users.py                     # Tests de CRUD + foto de perfil
│
├── .env.example                          # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup local

### 1. Clonar y crear entorno virtual

```bash
git clone <repo-url>
cd OptimusTrainingFastApi

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus valores reales:

```env
SECRET_KEY="genera-uno-con: openssl rand -hex 32"
SQLALCHEMY_DATABASE_URI="postgresql://usuario:contraseña@localhost/optimus_db"
```

### 4. Crear la base de datos (PostgreSQL)

```sql
CREATE DATABASE optimus_db;
```

### 5. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor arranca en **http://127.0.0.1:8000**

---

## 🧪 Tests

Los tests usan **SQLite en memoria** — no necesitas PostgreSQL para correrlos.

```bash
pytest tests/ -v
```

Resultado esperado:

```
15 passed in ~3s
```

---

## 📖 Endpoints — API v1

Toda la API vive bajo el prefijo `/api/v1`.

### 🔐 Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/api/v1/auth/login` | Login con email + password → JWT | ❌ |

**Body:**
```json
{
  "email": "usuario@email.com",
  "password": "MiContraseña123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### 👤 Usuarios

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/api/v1/users/` | Crear usuario | ❌ |
| `GET` | `/api/v1/users/` | Listar usuarios (paginado) | ✅ |
| `GET` | `/api/v1/users/me` | Mi perfil | ✅ |
| `GET` | `/api/v1/users/{id}` | Perfil por ID | ✅ |
| `PUT` | `/api/v1/users/{id}` | Actualizar perfil | ✅ (dueño) |
| `POST` | `/api/v1/users/{id}/photo` | Subir foto de perfil | ✅ (dueño) |
| `DELETE` | `/api/v1/users/{id}` | Eliminar usuario | ✅ (dueño) |

**Subir foto de perfil:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/1/photo" \
  -H "Authorization: Bearer <token>" \
  -F "file=@mi_foto.jpg"
```

La foto queda accesible en: `http://localhost:8000/uploads/profile_pictures/<nombre>.jpg`

---

### 📋 Reglas de validación

| Campo | Regla |
|---|---|
| `email` | Formato email válido |
| `password` | Mínimo 8 caracteres |
| `phone` | Regex: `+?[\d\s-]{7,15}` |
| `training_type` | Enum: `casa` \| `afuera` \| `gimnasio` \| `mixto` |
| `age` | Mayor a 0 |
| `weight` / `height` | Mayor a 0 |
| Foto de perfil | JPG, PNG, WEBP — máx 5 MB |

---

## 🔌 Documentación interactiva

| UI | URL |
|---|---|
| **Swagger UI** | http://127.0.0.1:8000/api/v1/docs |
| **ReDoc** | http://127.0.0.1:8000/api/v1/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/api/v1/openapi.json |

---

## 🧩 Cómo agregar un nuevo dominio (ej. `sports`)

Sigue este orden de capas para mantener consistencia:

```bash
# 1. Schema
app/schemas/sports/sport.py          # SportBase, SportCreate, SportResponse
app/schemas/sports/__init__.py       # exportar desde aquí

# 2. Model
app/models/sport.py                  # clase Sport(Base)
app/models/__init__.py               # agregar import de Sport

# 3. Service
app/services/sport_service.py        # SportService con métodos CRUD

# 4. Controller
app/controllers/sports/
    __init__.py
    sport_controller.py              # SportController con lógica HTTP

# 5. Route
app/api/v1/routes/sports.py          # endpoints thin que llaman al controller

# 6. Registrar en el router principal
# app/api/v1/router.py
api_router.include_router(sports.router, prefix="/sports", tags=["Deportes"])
```

---

## 🗄️ Migraciones con Alembic

Alembic es el equivalente de `prisma migrate` para Python + SQLAlchemy. Las migraciones son archivos `.py` versionados que describen los cambios en la base de datos.

### Flujo de trabajo diario

```bash
# 1. Activar entorno virtual
source .venv/bin/activate

# 2. Al cambiar / agregar un modelo, generar la migración automáticamente
alembic revision --autogenerate -m "descripcion_del_cambio"
# Ejemplo: alembic revision --autogenerate -m "add_sport_table"

# 3. Revisar el archivo generado en migrations/versions/ ← SIEMPRE hazlo
# Alembic es bueno pero a veces necesita ajuste manual

# 4. Aplicar la migración a la base de datos
alembic upgrade head
```

### Otros comandos útiles

```bash
# Ver el estado actual de migraciones
alembic current

# Ver el historial completo
alembic history --verbose

# Retroceder una migración (rollback)
alembic downgrade -1

# Retroceder a una revisión específica
alembic downgrade <revision_id>

# Retroceder TODO (base de datos limpia — ¡cuidado en producción!)
alembic downgrade base

# Generar SQL sin aplicarlo (útil para revisar antes de producción)
alembic upgrade head --sql > migration_preview.sql
```

### Agregar un nuevo modelo a las migraciones

Cuando crees un modelo nuevo (ej. `app/models/sport.py`), agrégalo en `migrations/env.py`:

```python
# migrations/env.py — sección de imports de modelos
from app.models import User          # ya está
from app.models.sport import Sport   # ← agrega esta línea
```

Luego corre:

```bash
alembic revision --autogenerate -m "add_sport_table"
alembic upgrade head
```

### Estructura de migrations/

```
migrations/
├── env.py           ← configuración (no tocar salvo para agregar modelos)
├── script.py.mako   ← plantilla de cada archivo de migración
├── README
└── versions/        ← archivos de migración (SÍ se suben a git)
    └── 20260225_1248-abc123_add_sport_table.py
```

> **Regla de oro**: Los archivos en `versions/` son el historial de tu base de datos — siempre súbelos a git junto con el código que los generó.

---

## 🔒 Seguridad en producción

- Cambia `SECRET_KEY` por un valor generado con `openssl rand -hex 32`
- Restringe `allow_origins` en CORS a tus dominios reales
- Usa HTTPS (Nginx + Certbot o un load balancer)
- Considera Redis para blacklist de tokens revocados
- Activa rate limiting (ej. `slowapi`)
