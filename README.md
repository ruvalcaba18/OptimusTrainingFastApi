# Optimus Training API 🏋️

API de deportes y entrenamiento construida con **FastAPI**, diseñada para escalar a **100 mil usuarios**. Sigue una arquitectura de capas clara: Routes → Controllers → Services → Database → Models.

---

## ✨ Características

- **Arquitectura de capas** — Routes, Controllers, Services, Database, Models con separación total de responsabilidades.
- **Versionado de API** — Toda la API vive bajo `/api/v1/`. Agregar `v2` no rompe nada.
- **3 módulos de negocio** — Enterprise (pausas activas), Coach (geolocalización + booking), Social (eventos + competencias).
- **Foto de perfil** — Endpoint dedicado para subir imagen JPG/PNG/WEBP (máx 5 MB) por usuario.
- **Archivos estáticos** — Las fotos se sirven en `/uploads/profile_pictures/` vía HTTP.
- **Pool de conexiones** — Configurado para alta concurrencia (`pool_size=10`, `max_overflow=20`).
- **Autenticación JWT** — Tokens Bearer con expiración configurable.
- **Validación estricta** — Pydantic v2 (email, teléfono regex, enum de tipo de entrenamiento).
- **Schemas comunes reutilizables** — `PaginatedResponse[T]` genérico y `MessageResponse`.
- **Documentación automática** — Swagger UI y ReDoc integrados.

---

## 🔒 Integridad de Datos — Principios ACID

Todos los módulos garantizan integridad ACID en operaciones críticas:

| Principio | Implementación |
|-----------|---------------|
| **Atomicity** | Patrón *Unit of Work* en controllers: `flush()` en el service, `commit()` único en el controller, `rollback()` en todo `except`. |
| **Consistency** | `UniqueConstraint` a nivel DB (ej. `uq_event_participant`), validaciones Pydantic v2 pre-persistencia, verificaciones de estado antes de mutar. |
| **Isolation** | `with_for_update()` (row-level lock) en operaciones concurrentes críticas: redención de código de empresa, join a evento/competencia con cupo, booking de coach. |
| **Durability** | PostgreSQL garantiza persistencia tras cada `COMMIT`. |

### Ejemplos de operaciones protegidas con row-level lock

- **Canje de código de empresa** — dos usuarios no pueden usar el mismo código simultáneamente.
- **Join a evento/competencia con cupo** — se bloquea la fila del evento para contar participantes antes de insertar.
- **Score update en competencia** — se bloquea la fila del participante para evitar escrituras concurrentes.
- **Booking de coach** — se bloquea el perfil del coach para verificar disponibilidad.

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
│   │   ├── deps.py                         # Dependencias reutilizables (get_current_user)
│   │   └── v1/
│   │       ├── router.py                   # Agrega todos los routers de v1
│   │       └── routes/                     # ← CAPA 1: solo declaran endpoints HTTP
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── enterprise.py           # Módulo Enterprise
│   │           ├── coaches.py              # Módulo Coach
│   │           ├── events.py              # Módulo Social — Eventos
│   │           └── competitions.py        # Módulo Social — Competencias
│   │
│   ├── controllers/                        # ← CAPA 2: lógica HTTP + autorización + ACID
│   │   ├── __init__.py
│   │   ├── auth/
│   │   ├── users/
│   │   ├── enterprise/
│   │   │   └── enterprise_controller.py
│   │   ├── coaches/
│   │   │   └── coach_controller.py
│   │   ├── events/
│   │   │   └── event_controller.py
│   │   └── competitions/
│   │       └── competition_controller.py
│   │
│   ├── services/                           # ← CAPA 3: data-access + row-level locks
│   │   ├── user_service.py
│   │   ├── upload_service.py
│   │   ├── enterprise_service.py
│   │   ├── coach_service.py
│   │   ├── event_service.py
│   │   └── competition_service.py
│   │
│   ├── database/                           # ← CAPA 4: configuración de DB
│   │   └── session/session.py
│   │
│   ├── models/                             # ← CAPA 5: modelos SQLAlchemy
│   │   ├── __init__.py                     # Importa todos los modelos (Alembic los detecta)
│   │   ├── user.py
│   │   ├── enterprise.py                   # Enterprise, EnterpriseCode, EnterpriseMember
│   │   ├── active_break.py                 # ActiveBreakSession, ActiveBreakLog
│   │   ├── coach.py                        # CoachProfile
│   │   ├── coach_booking.py                # CoachBooking
│   │   ├── event.py                        # Event, EventParticipant (UniqueConstraint)
│   │   └── competition.py                  # Competition, CompetitionParticipant (UniqueConstraint)
│   │
│   ├── schemas/                            # Pydantic — dividido por dominio
│   │   ├── users/
│   │   ├── common/
│   │   │   ├── pagination.py               # PaginatedResponse[T] genérico
│   │   │   └── response.py                 # MessageResponse
│   │   ├── enterprise/
│   │   │   ├── enterprise_enums.py         # BreakDuration, BreakCategory
│   │   │   ├── enterprise_schemas.py
│   │   │   └── active_break_schemas.py
│   │   ├── coaches/
│   │   │   ├── coach_enums.py              # CoachSpecialty, BookingStatus, SessionType
│   │   │   ├── coach_schemas.py
│   │   │   └── booking_schemas.py
│   │   ├── events/
│   │   │   ├── event_enums.py              # EventType, EventStatus
│   │   │   └── event_schemas.py
│   │   └── competitions/
│   │       ├── competition_enums.py        # CompetitionStatus
│   │       └── competition_schemas.py
│   │
│   └── main.py
│
├── tests/
├── migrations/
├── .env.example
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

### 5. Aplicar migraciones

```bash
alembic upgrade head
```

### 6. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor arranca en **http://127.0.0.1:8000**

---

## 📖 Endpoints — API v1

Toda la API vive bajo el prefijo `/api/v1`. Todos los endpoints marcados con ✅ requieren `Authorization: Bearer <token>`.

> **Convención REST**: Los IDs solo aparecen al final del path (`/resource/{id}`). Los IDs de contexto van como query params (GET) o en el body (POST/PUT).

---

### 🔐 Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/auth/login` | Login con email + password → JWT | ❌ |
| `POST` | `/auth/login/access-token` | Login compatible con Swagger | ❌ |
| `POST` | `/auth/refresh-token` | Refrescar access token | ❌ |
| `POST` | `/auth/password-recovery/{email}` | Iniciar recuperación | ❌ |
| `POST` | `/auth/reset-password` | Restablecer con token | ❌ |

---

### 👤 Usuarios

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/users/` | Crear usuario | ❌ |
| `GET` | `/users/` | Listar usuarios (paginado) | ✅ |
| `GET` | `/users/me` | Mi perfil | ✅ |
| `GET` | `/users/{id}` | Perfil por ID | ✅ |
| `PUT` | `/users/{id}` | Actualizar perfil | ✅ dueño |
| `POST` | `/users/{id}/photo` | Subir foto de perfil | ✅ dueño |
| `DELETE` | `/users/{id}` | Eliminar usuario | ✅ dueño |

---

### 🏢 Enterprise — Pausas Activas

Valida que un empleado pertenece a una empresa mediante un **código de un solo uso** que expira.

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/enterprise/` | Crear empresa | ✅ |
| `GET` | `/enterprise/my-enterprise` | Ver mi empresa | ✅ |
| `POST` | `/enterprise/validate-code` | Canjear código de empresa (**ACID lock**) | ✅ |
| `POST` | `/enterprise/codes` | Generar N códigos (`enterprise_id` en body) | ✅ |
| `GET` | `/enterprise/codes` | Listar códigos (`enterprise_id` en query) | ✅ |
| `GET` | `/enterprise/members` | Listar miembros (`enterprise_id` en query) | ✅ |
| `POST` | `/enterprise/active-breaks` | Crear plantilla de pausa activa | ✅ |
| `GET` | `/enterprise/active-breaks` | Listar pausas (filtro: `duration`, `category`) | ✅ |
| `GET` | `/enterprise/active-breaks/{id}` | Detalle de pausa | ✅ |
| `POST` | `/enterprise/break-logs` | Iniciar pausa (`session_id` en body) | ✅ |
| `PUT` | `/enterprise/break-logs/{id}` | Completar pausa | ✅ |
| `GET` | `/enterprise/my-stats` | Estadísticas personales de pausas | ✅ |

**Flujo de validación de código:**
```json
POST /api/v1/enterprise/validate-code
{ "code": "A3K9-M2X7" }
```
- El código se busca con **row-level lock** (`SELECT ... FOR UPDATE`).
- Si es válido, no usado y no expirado → usuario se vincula a la empresa.
- El código queda marcado como `is_used = true` — no puede reusarse.

**Duraciones de pausa:** `10` | `20` | `30` minutos  
**Categorías:** `stretching` | `cardio` | `strength` | `mindfulness` | `mobility`

---

### 🏅 Coach — Coaches y Booking

Los coaches se muestran en un mapa usando la fórmula de **Haversine** para calcular distancia.

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/coaches/` | Registrarse como coach | ✅ |
| `GET` | `/coaches/` | Listar coaches (filtro: `specialty`) | ✅ |
| `GET` | `/coaches/nearby` | **Buscar en mapa** (`lat`, `lng`, `radius_km`) | ✅ |
| `GET` | `/coaches/{id}` | Ver perfil de coach | ✅ |
| `PUT` | `/coaches/{id}` | Actualizar perfil (solo dueño) | ✅ |
| `DELETE` | `/coaches/{id}` | Desactivar perfil (soft delete) | ✅ |
| `POST` | `/coaches/bookings` | Solicitar sesión (`coach_id` en body) | ✅ |
| `GET` | `/coaches/bookings/my-sessions` | Mis sesiones como atleta | ✅ |
| `GET` | `/coaches/bookings/my-clients` | Mis clientes como coach | ✅ |
| `PUT` | `/coaches/bookings/{id}` | Aceptar / rechazar sesión (solo coach) | ✅ |
| `POST` | `/coaches/reviews` | Calificar sesión (`booking_id` en body) | ✅ |

**Búsqueda por mapa:**
```
GET /api/v1/coaches/nearby?lat=19.4326&lng=-99.1332&radius_km=15&specialty=running
```
Retorna cada coach con `distance_km` calculada, ordenados del más cercano al más lejano.

**Precio automático al crear booking:**
```
total_price = hourly_rate × (duration_minutes / 60)
```

**Rating automático tras review:**  
El `avg_rating` y `total_reviews` del coach se recalculan automáticamente.

**Especialidades:** `personal_trainer` | `yoga` | `crossfit` | `running` | `swimming` | `nutrition` | `physiotherapy` | `strength` | `functional` | `other`

**Estados de booking:** `pending` → `accepted` | `rejected` → `completed`

---

### 🎉 Social — Eventos

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/events/` | Crear evento | ✅ |
| `GET` | `/events/` | Listar eventos (filtro: `event_type`, `status`) | ✅ |
| `GET` | `/events/{id}` | Detalle con conteo de participantes | ✅ |
| `PUT` | `/events/{id}` | Actualizar evento (solo creador) | ✅ |
| `DELETE` | `/events/{id}` | Cancelar evento (soft cancel) | ✅ |
| `POST` | `/events/participants` | Unirse a evento (`event_id` en body, **ACID lock**) | ✅ |
| `DELETE` | `/events/participants` | Salir de evento (`event_id` en body) | ✅ |
| `GET` | `/events/participants/list` | Listar participantes (`event_id` en query) | ✅ |

**ACID en join:**  
Se bloquea la fila del evento (`SELECT ... FOR UPDATE`) para validar el cupo antes de insertar. Si el evento tiene `max_participants`, nadie puede excederlo por concurrencia.

**Tipos de evento:** `running` | `cycling` | `swimming` | `crossfit` | `yoga` | `hiking` | `other`

---

### 🏆 Social — Competencias

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/competitions/` | Crear competencia | ✅ |
| `GET` | `/competitions/` | Listar (filtro: `sport_type`, `status`) | ✅ |
| `GET` | `/competitions/{id}` | Detalle de competencia | ✅ |
| `PUT` | `/competitions/{id}` | Actualizar (solo creador) | ✅ |
| `POST` | `/competitions/participants` | Inscribirse (`competition_id` en body, **ACID lock**) | ✅ |
| `PUT` | `/competitions/scores` | Actualizar score (**idempotente**, solo creador) | ✅ |
| `GET` | `/competitions/ranking` | Ver ranking (`competition_id` en query) | ✅ |

**ACID en inscripción:**  
Se bloquea la fila de la competencia durante la inscripción para validar cupo con exactitud.

**Idempotencia en scores:**  
`PUT /competitions/scores` sigue semántica PUT — llamarlo dos veces con el mismo score produce el mismo resultado. Las posiciones se recalculan automáticamente después de cada actualización.

**Estados:** `upcoming` → `in_progress` → `finished` | `cancelled`

---

## 🗄️ Migraciones con Alembic

```bash
# Al agregar nuevos modelos, generar la migración
alembic revision --autogenerate -m "nombre_del_cambio"

# Aplicar
alembic upgrade head

# Rollback de una migración
alembic downgrade -1

# Ver estado actual
alembic current

# Ver historial
alembic history --verbose
```

### Migración completa (todos los módulos)

```bash
alembic revision --autogenerate -m "add_enterprise_coach_social_modules"
alembic upgrade head
```

Esto creará las tablas:
- `enterprises`, `enterprise_codes`, `enterprise_members`
- `active_break_sessions`, `active_break_logs`
- `coach_profiles`, `coach_bookings`
- `events`, `event_participants`
- `competitions`, `competition_participants`

---

## 🔌 Documentación interactiva

| UI | URL |
|---|---|
| **Swagger UI** | http://127.0.0.1:8000/api/v1/docs |
| **ReDoc** | http://127.0.0.1:8000/api/v1/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/api/v1/openapi.json |

---

## 🧩 Cómo agregar un nuevo dominio

Sigue este orden de capas:

```bash
# 1. Schema
app/schemas/nuevo_dominio/__init__.py
app/schemas/nuevo_dominio/enums.py
app/schemas/nuevo_dominio/schemas.py

# 2. Model
app/models/nuevo_dominio.py          # clase(Base) con UniqueConstraint donde aplique
app/models/__init__.py               # agregar import

# 3. Service  (flush, not commit — con with_for_update() en operaciones críticas)
app/services/nuevo_dominio_service.py

# 4. Controller  (commit/rollback aquí, validaciones ACID)
app/controllers/nuevo_dominio/
    __init__.py
    nuevo_dominio_controller.py

# 5. Route  (thin layer — solo HTTP in/out)
app/api/v1/routes/nuevo_dominio.py

# 6. Registrar
# app/api/v1/router.py
api_router.include_router(nuevo_dominio.router, prefix="/nuevo-dominio", tags=["..."])
```

---

## 🔒 Seguridad en producción

- Cambia `SECRET_KEY` por un valor generado con `openssl rand -hex 32`
- Restringe `allow_origins` en CORS a tus dominios reales
- Usa HTTPS (Nginx + Certbot o un load balancer)
- Considera Redis para blacklist de tokens revocados
- Activa rate limiting (ej. `slowapi`)
