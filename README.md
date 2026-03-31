# Optimus Training API 🏋️

API de deportes y entrenamiento construida con **FastAPI + PostgreSQL + Redis**, diseñada para escalar a **1 millón de usuarios**. Arquitectura de capas: Routes → Controllers → Services → Database → Models.

---

## ✨ Características

- **Arquitectura de 5 capas** — Routes, Controllers, Services, Database, Models con separación total de responsabilidades.
- **Autenticación JWT** completa — Access token + Refresh token + Recuperación de contraseña.
- **Social Auth** — Sign In con Apple, Google y Facebook (validación server-side, sin depender del cliente).
- **Redis Cache** — Nearest coaches (Haversine), rankings, catálogo de pausas activas. Falla silenciosamente si Redis no está disponible.
- **Rate Limiting** — `slowapi` con `200 req/min` por IP por defecto.
- **Error Handling Unificado** — Todos los errores retornan `{"error": {"code": "...", "message": "..."}}`.
- **OWASP Top 10** — Ver sección de seguridad.
- **Pool de conexiones** — `pool_size=20`, `max_overflow=40` para alta concurrencia.
- **ACID en operaciones críticas** — Row-level locks en bookings, join a eventos, canje de códigos.
- **Logging estructurado** — `logs/access.log` y `logs/errors.log` con rotación automática.
- **55 tests unitarios** — Cobertura de auth, social auth, users, providers, security.

---

## 🔒 OWASP Top 10 — Estado del proyecto

| # | Riesgo | Estado | Implementación |
|---|--------|--------|----------------|
| A01 | Broken Access Control | ✅ | `get_current_user` en cada endpoint, validación de ownership en controller |
| A02 | Cryptographic Failures | ✅ | `bcrypt` para passwords, JWT HS256 con SECRET_KEY requerido del `.env` |
| A03 | Injection | ✅ | SQLAlchemy ORM — nunca SQL crudo con input del usuario |
| A04 | Insecure Design | ✅ | Rate limiting `slowapi`, ACID con row-level locks |
| A05 | Security Misconfiguration | ✅ | CORS configurable por env, headers: `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection` |
| A06 | Vulnerable Components | ⚠️ | Ejecutar `pip-audit` periódicamente |
| A07 | Authentication Failures | ✅ | Token expiry, refresh token, blacklist (Redis), validación estricta |
| A08 | Data Integrity Failures | ✅ | Pydantic v2 pre-persistencia, `UniqueConstraint` en DB |
| A09 | Logging and Monitoring | ✅ | Access log + error log con `RotatingFileHandler`, códigos de error estructurados |
| A10 | SSRF | ✅ | httpx con timeout configurado en llamadas a Apple/Google/Facebook |

---

## 🗄️ Redis — Estrategia de Cache

Redis falla **silenciosamente** — si el servidor no está disponible, la app sigue funcionando sin cache.

| Endpoint | Clave | TTL | Por qué |
|---|---|---|---|
| `GET /coaches/nearby` | `coaches:nearby:{lat}:{lng}:{radius}:{specialty}` | **3 min** | Query Haversine más costosa del proyecto — SQL trigonométrico sobre todos los coaches |
| `GET /coaches/{id}` | `coach:profile:{id}` | **5 min** | Perfil leído frecuentemente, rara vez actualizado |
| `GET /competitions/ranking` | `ranking:{competition_id}` | **1 min** | Recalcula posiciones sobre todos los participantes |
| `POST /competitions/scores` | invalidar `ranking:{id}` | — | Cache bust inmediato al actualizar un score |
| `GET /enterprise/active-breaks` | `active_breaks:{duration}:{category}` | **10 min** | Catálogo casi estático, consultado por todos los empleados |
| `POST /enterprise/active-breaks` | invalidar `active_breaks:*` | — | Cache bust cuando se crea una nueva pausa |

**Token blacklisting** (logout):
```
blacklist:{jti}  →  TTL = tiempo restante del token
```

---

## 🛠️ Stack tecnológico

| Librería | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web principal |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM + connection pool |
| [PostgreSQL](https://www.postgresql.org/) | Base de datos principal |
| [Redis](https://redis.io/) | Cache + rate limit + token blacklist |
| [Pydantic v2](https://docs.pydantic.dev/) | Validación y serialización |
| [Python-JOSE](https://python-jose.readthedocs.io/) | JWT (HS256) |
| [Passlib + bcrypt](https://passlib.readthedocs.io/) | Hash seguro de contraseñas |
| [slowapi](https://github.com/laurentS/slowapi) | Rate limiting por IP |
| [httpx](https://www.python-httpx.org/) | HTTP async para social auth |
| [pytest + pytest-asyncio](https://docs.pytest.org/) | Suite de tests (55 tests) |

---

## 📁 Estructura del proyecto

```
OptimusTrainingFastApi/
│
├── app/
│   ├── api/
│   │   ├── deps.py                         # get_current_user (JWT decode)
│   │   └── v1/
│   │       ├── router.py
│   │       └── routes/                     # CAPA 1 — HTTP in/out + cache async
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── social_auth.py          # Apple / Google / Facebook
│   │           ├── enterprise.py           # Cache: active-breaks (10 min)
│   │           ├── coaches.py              # Cache: nearby (3 min), profile (5 min)
│   │           ├── events.py
│   │           ├── competitions.py         # Cache: ranking (1 min)
│   │           └── training.py
│   │
│   ├── controllers/                        # CAPA 2 — lógica HTTP + autorización + ACID
│   │   ├── auth/
│   │   │   ├── auth_controller.py
│   │   │   └── social_auth_controller.py
│   │   ├── users/
│   │   ├── enterprise/
│   │   ├── coaches/
│   │   ├── events/
│   │   ├── competitions/
│   │   └── training_controller.py
│   │
│   ├── services/                           # CAPA 3 — data-access + row-level locks
│   │   ├── user_service.py
│   │   ├── upload_service.py
│   │   ├── enterprise_service.py
│   │   ├── coach_service.py
│   │   ├── event_service.py
│   │   ├── competition_service.py
│   │   ├── training_service.py
│   │   └── social_auth/
│   │       ├── apple_provider.py
│   │       ├── google_provider.py
│   │       └── facebook_provider.py
│   │
│   ├── database/                           # CAPA 4 — DB (pool_size=20, max_overflow=40)
│   │   └── session/session.py
│   │
│   ├── models/                             # CAPA 5 — SQLAlchemy models
│   │   ├── user.py
│   │   ├── enterprise.py
│   │   ├── active_break.py
│   │   ├── coach.py
│   │   ├── coach_booking.py
│   │   ├── event.py
│   │   ├── competition.py
│   │   └── training.py
│   │
│   ├── schemas/                            # Pydantic v2 — por dominio
│   │
│   ├── core/
│   │   ├── config.py                       # Settings (pydantic-settings)
│   │   ├── security.py                     # JWT + bcrypt
│   │   ├── middleware.py                   # SecurityMiddleware (headers + logging)
│   │   ├── redis_client.py                 # Redis connection + blacklist
│   │   ├── cache.py                        # cache_get / cache_set / cache_delete
│   │   ├── error_handlers.py               # Todos los exception handlers
│   │   └── logging_config.py              # RotatingFileHandler
│   │
│   └── main.py                             # FastAPI app + lifespan + rate limiter
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_social_auth.py
│   ├── test_unit.py
│   └── test_users.py
├── logs/                                   # access.log + errors.log (auto-creado)
├── migrations/
├── .env
└── requirements.txt
```

---

## 🚀 Setup local

### 1. Clonar y crear entorno virtual

```bash
git clone <repo-url>
cd OptimusTrainingFastApi

python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Redis (requerido para cache y rate limiting)

```bash
# macOS
brew install redis && brew services start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Variables **requeridas** (sin default — la app no arranca sin ellas):

```env
SECRET_KEY="genera-uno-con: openssl rand -hex 32"
SQLALCHEMY_DATABASE_URI="postgresql://usuario:password@localhost/optimus_db"
```

Variables opcionales:

```env
REDIS_URL="redis://localhost:6379/0"
RATE_LIMIT_ENABLED=true
ALLOWED_ORIGINS=["https://tudominio.com","https://app.tudominio.com"]

# Social Auth
APPLE_CLIENT_ID="com.tuempresa.optimus"
GOOGLE_CLIENT_ID="xxxx.apps.googleusercontent.com"
FACEBOOK_APP_ID="xxxx"
FACEBOOK_APP_SECRET="xxxx"
```

### 5. Base de datos

```sql
CREATE DATABASE optimus_db;
```

```bash
alembic upgrade head
```

### 6. Iniciar servidor

```bash
uvicorn app.main:app --reload
```

El servidor arranca en **http://127.0.0.1:8000**

---

## 🧪 Tests

```bash
# Correr todos los tests (SQLite in-memory, sin PostgreSQL ni Redis)
python -m pytest tests/ -v

# Con cobertura
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=term-missing
```

**55 tests — 4 archivos:**

| Archivo | Tests | Qué cubre |
|---|---|---|
| `test_auth.py` | 8 | Login, refresh token, casos de error |
| `test_social_auth.py` | 15 | Apple/Google/Facebook — nuevo usuario, existente, desactivado |
| `test_unit.py` | 15 | JWT tokens, bcrypt, providers (mocked HTTP) |
| `test_users.py` | 17 | CRUD completo, permisos, validaciones, foto de perfil |

---

## 📖 Endpoints — API v1

Todos bajo `/api/v1`. Los que tienen ✅ requieren `Authorization: Bearer <token>`.

### 🔐 Autenticación

| Método | Ruta | Auth |
|--------|------|------|
| `POST` | `/auth/login` | ❌ |
| `POST` | `/auth/login/access-token` | ❌ |
| `POST` | `/auth/refresh-token` | ❌ |
| `POST` | `/auth/password-recovery/{email}` | ❌ |
| `POST` | `/auth/reset-password` | ❌ |
| `POST` | `/auth/social/{provider}` | ❌ — `provider`: `apple` \| `google` \| `facebook` |

### 👤 Usuarios

| Método | Ruta | Auth |
|--------|------|------|
| `POST` | `/users/` | ❌ |
| `GET` | `/users/` | ✅ |
| `GET` | `/users/me` | ✅ |
| `GET` | `/users/{id}` | ✅ |
| `PUT` | `/users/{id}` | ✅ dueño |
| `POST` | `/users/{id}/photo` | ✅ dueño |
| `DELETE` | `/users/{id}` | ✅ dueño |

### 🏢 Enterprise, 🏅 Coach, 🎉 Events, 🏆 Competencias, 🏋️ Training

Ver `/api/v1/docs` para la documentación interactiva completa.

---

## 🗄️ Migraciones

```bash
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
alembic downgrade -1
alembic current
```

---

## 🔒 Seguridad en producción

```bash
# Checks recomendados antes de deploy
pip install pip-audit
pip-audit                          # Audita dependencias con CVEs conocidos

openssl rand -hex 32               # Generar SECRET_KEY seguro
```

- `SECRET_KEY` y `SQLALCHEMY_DATABASE_URI` son requeridos — la app falla inmediatamente si no están
- `ALLOWED_ORIGINS` — restringir a tus dominios reales (no `["*"]`)
- HTTPS obligatorio en producción (Nginx + Certbot o load balancer con TLS)
- Redis en producción con autenticación: `redis://:password@host:6379/0`
- Rate limit ajustable por IP — considerar `100/minute` en producción
