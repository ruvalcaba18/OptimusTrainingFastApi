# Optimus Training API 🏋️

API de deportes y entrenamiento construida con **FastAPI + PostgreSQL + Redis**, diseñada para escalar a **1 millón de usuarios**. Implementa una arquitectura robusta de 5 capas organizada por dominios y un completo motor de decisión inteligente para la generación de rutinas personalizadas.

---

## ✨ Características Principales

- **Arquitectura de 5 capas modular** — Separación estricta de responsabilidades (Routes → Controllers → Services → Database → Models) organizada por dominios para facilitar el mantenimiento y escalabilidad.
- **Motor de Decisión de Ejercicios (Fase 6)** — Selección y filtrado dinámico de ejercicios considerando nivel del usuario, equipamiento disponible y restricciones de salud (patologías y enfermedades) que descartan ejercicios prohibidos (`FORBIDDEN`) y agregan advertencias (`CAUTION`).
- **Generador Inteligente de Rutinas (Fase 7)** — Generación automatizada de rutinas basadas en el perfil de usuario y una **Matriz de Programación** que determina el volumen, series (sets), repeticiones, descanso y métodos de entrenamiento idóneos de forma personalizada.
- **Asistente de Inteligencia Artificial (OpenAI Proxy)** — Integración de chat inteligente para consultas de entrenamiento y salud deportiva, controlado por un **Rate Limiter Global en Redis** (máximo 100 consultas).
- **Dashboard de Auditoría de Prompts** — Registro persistente en base de datos (`prompt_logs`) de todas las interacciones con la IA, expuesto de forma segura en un endpoint de visualización exclusivo para usuarios administradores.
- **Autenticación Completa y JWT** — Flujo seguro de login, registro, recuperación de contraseña y renovación de tokens (Access token + Refresh token).
- **Social Auth Server-Side** — Validación directa y segura de tokens con proveedores externos: **Apple, Google y Facebook**.
- **Redis Cache & Blacklist** — Caché asíncrona para endpoints costosos (búsqueda Haversine de coaches, rankings de competencias, pausas activas) y almacenamiento de tokens invalidados. Falla de manera silenciosa si Redis no está disponible.
- **OWASP Top 10 y Seguridad** — Rate limiting por IP con `slowapi`, headers de seguridad, sanitización de entradas, prevención de inyecciones SQL usando SQLAlchemy ORM y timeouts en llamadas HTTP.
- **Carga de Datos Maestros (Seed)** — Carga automatizada desde archivos tabulares (.tsv) para poblar el catálogo de ejercicios, equipamiento, métodos de entrenamiento y la matriz de programación.
- **66 Tests Automatizados** — Suite de pruebas unitarias y de integración que aseguran la consistencia de la autenticación, flujos de usuarios, exclusiones médicas y el generador de rutinas.

---

## 🔒 OWASP Top 10 — Estado del proyecto

| # | Riesgo | Estado | Implementación |
|---|--------|--------|----------------|
| **A01** | Broken Access Control | ✅ | Validación de ownership en controladores y verificación de tokens en dependencias de FastAPI (`get_current_user`). |
| **A02** | Cryptographic Failures | ✅ | Uso de `bcrypt` para contraseñas y firmas JWT HS256 con claves simétricas secretas obligatorias. |
| **A03** | Injection | ✅ | Sanitización completa mediante SQLAlchemy ORM (evitando SQL crudo con inputs directos). |
| **A04** | Insecure Design | ✅ | Rate limiting dinámico (`slowapi`), concurrencia protegida mediante Row-Level Locks (`with_for_update`) en transacciones críticas. |
| **A05** | Security Misconfiguration | ✅ | Orígenes CORS estrictamente definidos por entorno y headers de seguridad (`X-Frame-Options`, `X-Content-Type-Options`). |
| **A06** | Vulnerable Components | ⚠️ | Monitorizado periódicamente usando herramientas como `pip-audit`. |
| **A07** | Authentication Failures | ✅ | Blacklist de tokens en Redis al cerrar sesión, tokens de corta duración y validación estricta. |
| **A08** | Data Integrity Failures | ✅ | Validación estricta con Pydantic v2 en datos de entrada y restricciones de base de datos (`UniqueConstraint`). |
| **A09** | Security Logging & Monitoring | ✅ | Logs estructurados rotativos (`logs/access.log` y `logs/errors.log`) con detalles específicos de errores y auditoría de prompts de la IA. |
| **A10** | SSRF | ✅ | Uso de `httpx` con políticas de timeouts estrictas para integraciones con Apple, Google y Facebook. |

---

## 🗄️ Redis — Estrategia de Cache y Rate Limit

La integración con Redis está diseñada para fallar **silenciosamente**. Si Redis se desconecta, la API redirige las solicitudes directamente a la base de datos sin interrumpir el servicio.

### 1. Claves de Cache

| Endpoint | Clave en Redis | TTL | Razón de Uso |
|---|---|---|---|
| `GET /coaches/nearby` | `coaches:nearby:{lat}:{lng}:{radius}:{specialty}` | **3 min** | Evita recalcular consultas Haversine costosas sobre la base de datos. |
| `GET /coaches/{id}` | `coach:profile:{id}` | **5 min** | Información de perfil de lectura frecuente y actualización esporádica. |
| `GET /competitions/ranking` | `ranking:{competition_id}` | **1 min** | Cachea el cálculo de puntajes acumulados de todos los participantes. |
| `POST /competitions/scores` | *Invalida* `ranking:{id}` | — | Cache-bust inmediato al actualizar la puntuación de un competidor. |
| `GET /enterprise/active-breaks` | `active_breaks:{duration}:{category}` | **10 min** | Catálogo semiestático consumido concurrentemente por múltiples usuarios corporativos. |
| `POST /enterprise/active-breaks` | *Invalida* `active_breaks:*` | — | Cache-bust inmediato al crear o modificar pausas activas. |

### 2. Control de Acceso e IA
- **Token Blacklisting**: `blacklist:{jti}` almacenado con un TTL correspondiente al tiempo de vida restante del token JWT.
- **Rate Limit de Chat**: Control global mediante la clave `global_chat_calls_lifetime_count` (Límite configurado en un máximo de **100** solicitudes de por vida).

---

## 🛠️ Stack Tecnológico

- **FastAPI**: Framework web asíncrono y de alto rendimiento.
- **SQLAlchemy (V2)**: ORM y pool de conexiones configurado para alta concurrencia (`pool_size=20`, `max_overflow=40`).
- **Alembic**: Sistema de migraciones de base de datos estructurado.
- **PostgreSQL**: Base de datos principal relacional para producción.
- **Redis**: Capa de caché en memoria, rate limiting y almacenamiento de tokens invalidados.
- **Pydantic V2**: Validación estricta y serialización veloz de esquemas.
- **Passlib & BCrypt**: Hash seguro de contraseñas de usuarios.
- **Python-JOSE**: Creación, firma y verificación de tokens JSON Web Tokens (JWT).
- **Httpx**: Cliente HTTP asíncrono utilizado para verificar tokens de Social Auth.
- **Slowapi**: Middleware para aplicar límites de peticiones (Rate Limiting) por dirección IP.
- **Pytest & Pytest-Asyncio**: Suite de testing asíncrono.

---

## 📁 Estructura del Proyecto (Arquitectura de Capas por Dominio)

```
OptimusTrainingFastApi/
│
├── app/
│   ├── api/
│   │   ├── deps.py                         # Dependencias compartidas (get_db, get_current_user)
│   │   └── v1/
│   │       ├── router.py                   # Enrutador principal de la API v1
│   │       └── routes/                     # Capa 1 — Controladores de ruta (HTTP In/Out y Cache Async)
│   │           ├── auth.py                 # Login tradicional, refresh y recovery
│   │           ├── social_auth.py          # Autenticación con Apple, Google y Facebook
│   │           ├── users.py                # CRUD de usuarios y subida de fotos
│   │           ├── enterprise.py           # Gestión y logs de pausas activas
│   │           ├── coaches.py              # Perfiles de coaches y geolocalización Haversine
│   │           ├── training.py             # Gestión manual de planes y entrenamientos
│   │           ├── excersices.py           # Catálogo de ejercicios, niveles, objetivos y restricciones
│   │           ├── routines.py             # Generador automático de rutinas personalizadas
│   │           ├── chat.py                 # Endpoint de chat para asistente de IA
│   │           ├── prompt_logs.py          # Dashboard de logs de prompts (solo administradores)
│   │           ├── events.py               # Gestión de eventos deportivos y reservas
│   │           └── competitions.py         # Rankings e inscripciones a competencias
│   │
│   ├── controllers/                        # Capa 2 — Lógica de presentación, autorizaciones y transacciones ACID
│   │   ├── auth/                           # Controladores de autenticación tradicional y social
│   │   ├── users/                          # Lógica de operaciones de usuario
│   │   ├── enterprise/                     # Controladores de pausas corporativas
│   │   ├── coaches/                        # Controladores de interacción con coaches
│   │   ├── excersices/                     # Controladores del catálogo deportivo
│   │   ├── chat/                           # Lógica del asistente e inserción de logs de prompts
│   │   ├── competitions/                   # Controladores para rankings y puntajes
│   │   ├── events/                         # Lógica de reservas y asistencias a eventos
│   │   └── training_controller.py          # Lógica de planes y workouts manuales
│   │
│   ├── services/                           # Capa 3 — Lógica de negocio pura, algoritmos y accesos a datos maestros
│   │   ├── user/                           # Servicios de usuario, envío de emails y carga de archivos
│   │   ├── enterprise/                     # Lógica de pausas activas corporativas
│   │   ├── coach/                          # Servicios de coaches
│   │   ├── social/                         # Servicios de competencias y eventos
│   │   ├── excersice/                      # Servicios para catalogar niveles, objetivos, métodos y condiciones
│   │   ├── training/                       # Generador de rutinas y selector de ejercicios inteligente
│   │   │   ├── routine_generator.py        # Aplica la matriz de programación (volumen, descanso, series)
│   │   │   └── exercise_selector.py        # Filtra ejercicios por nivel, equipamiento y patologías/enfermedades
│   │   ├── chat/                           # Conector Proxy con OpenAI y contador de Redis
│   │   └── uploads/                        # Directorio local temporal para subidas de archivos
│   │
│   ├── database/                           # Capa 4 — Configuración e inicialización de la Base de Datos
│   │   ├── session/session.py              # Conexión principal y configuración del pool
│   │   ├── data/                           # Archivos de datos maestros (.tsv) para la inicialización
│   │   └── seed_all.py                     # Script para limpiar y sembrar datos maestros en la base de datos
│   │
│   ├── models/                             # Capa 5 — Modelos SQLAlchemy y mapeo de tablas relacionales
│   │   ├── Enums/                          # Enums de estado de planes, workouts y patrones de ejercicio
│   │   ├── user/                           # User, UserProfile, UserDisease, UserPathology, UserEquipment
│   │   ├── enterprise/                     # Enterprise, EnterpriseCode, EnterpriseMember, ActiveBreakSession/Log
│   │   ├── coach/                          # CoachProfile, CoachBooking, CoachAthlete
│   │   ├── excersice/                      # Excersice, Level, Goal, Condition, Method, Equipment, etc.
│   │   ├── training/                       # TrainingPlan, DailyWorkout, ExerciseDetail, ProgrammingMatrix
│   │   ├── social/                         # Event, EventParticipant, Competition, CompetitionParticipant
│   │   └── prompt_log/                     # PromptLog (Historial de consultas de la IA)
│   │
│   ├── schemas/                            # Modelos Pydantic v2 organizados por dominio
│   │   ├── users/
│   │   ├── enterprise/
│   │   ├── coaches/
│   │   ├── sports/
│   │   ├── training/
│   │   ├── chat/
│   │   ├── prompts/
│   │   ├── events/
│   │   ├── competitions/
│   │   └── common/
│   │
│   ├── core/                               # Configuración global, middlewares y utilidades transversales
│   │   ├── config.py                       # Carga y validación de variables de entorno (.env)
│   │   ├── security.py                     # Funciones criptográficas (bcrypt, creación y decodificación de JWT)
│   │   ├── middleware.py                   # Inyección de headers de seguridad y logging de accesos
│   │   ├── redis_client.py                 # Conexión cliente Redis
│   │   ├── cache.py                        # Helpers genéricos de lectura, escritura y borrado de caché
│   │   ├── error_handlers.py               # Capturador unificado de excepciones y formato estructurado
│   │   └── logging_config.py               # Configuración estructurada de RotatingFileHandlers para logs
│   │
│   └── main.py                             # Inicialización de la aplicación FastAPI, Lifespan y Middlewares
│
├── tests/                                  # Suite completa de pruebas automatizadas
│   ├── conftest.py                         # Fixtures de base de datos SQLite en memoria y cliente de pruebas
│   ├── test_auth.py                        # Tests de flujos de autenticación tradicional
│   ├── test_social_auth.py                 # Tests para integraciones con Apple, Google y Facebook
│   ├── test_users.py                       # Tests del CRUD de usuarios y cargas de fotos de perfil
│   ├── test_excersices.py                  # Tests de consulta de catálogo de ejercicios y filtros dinámicos
│   ├── test_routines.py                    # Tests de generación automática y validación de restricciones
│   └── test_unit.py                        # Pruebas unitarias de tokens y validaciones de mock de providers
│
├── logs/                                   # Carpeta auto-generada para archivos access.log y errors.log
├── migrations/                             # Historial de migraciones generadas por Alembic
├── .env.example                            # Plantilla de variables de entorno requeridas
└── requirements.txt                        # Lista de dependencias del proyecto
```

---

## 🚀 Instalación y Configuración Local

### 1. Clonar el repositorio y crear el entorno virtual
```bash
git clone <repo-url>
cd OptimusTrainingFastApi

python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias requeridas
```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor Redis
Redis es **requerido** para habilitar la caché de endpoints costosos, el rate limiting y el límite de pruebas del chat de IA.
```bash
# En macOS usando Homebrew
brew install redis
brew services start redis

# O ejecutándolo mediante Docker
docker run -d -p 6379:6379 redis:alpine
```

### 4. Configurar variables de entorno
Crea una copia de la plantilla `.env.example` con el nombre `.env`:
```bash
cp .env.example .env
```

Define las siguientes variables **obligatorias** (la aplicación fallará al iniciar si no se definen):
```env
SECRET_KEY="genera-un-string-seguro-con: openssl rand -hex 32"
SQLALCHEMY_DATABASE_URI="postgresql://usuario:password@localhost/optimus_db"
```

Configura variables **opcionales** (según necesidades de desarrollo/producción):
```env
REDIS_URL="redis://localhost:6379/0"
RATE_LIMIT_ENABLED=true
ALLOWED_ORIGINS=["https://tudominio.com","https://app.tudominio.com"]

# Credenciales de API de Terceros
OPENAI_API_KEY="tu-api-key-de-openai"

# Credenciales de Autenticación Social
APPLE_CLIENT_ID="com.tuempresa.optimus"
GOOGLE_CLIENT_ID="xxxx.apps.googleusercontent.com"
FACEBOOK_APP_ID="xxxx"
FACEBOOK_APP_SECRET="xxxx"
```

### 5. Base de Datos: Crear y Migrar
Crea la base de datos PostgreSQL local (por ejemplo, con `pgAdmin` o `psql`):
```sql
CREATE DATABASE optimus_db;
```

Ejecuta las migraciones de Alembic para crear la estructura de tablas correspondiente:
```bash
alembic upgrade head
```

### 6. Cargar Datos Maestros (Seeding)
Puebla las tablas de base de datos con los datos iniciales requeridos (niveles, objetivos, condiciones médicas, equipamientos, métodos, catálogo de ejercicios y matriz de programación):
```bash
python -m app.database.seed_all
```

### 7. Iniciar el Servidor de Desarrollo
```bash
uvicorn app.main:app --reload
```
La API estará disponible e interactiva en: **http://127.0.0.1:8000**  
Puedes consultar la documentación auto-generada de OpenAPI en: **http://127.0.0.1:8000/docs**

---

## 🧪 Pruebas Automatizadas (Tests)

Las pruebas están configuradas para ejecutarse sobre una base de datos SQLite en memoria aislada, por lo que no requieren tener PostgreSQL ni Redis activos para completarse.

```bash
# Ejecutar todas las pruebas en modo detallado
python -m pytest tests/ -v

# Ejecutar pruebas con reporte de cobertura de código
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=term-missing
```

### Detalle de los 66 Tests:

| Módulo de Pruebas | N° de Tests | Cobertura Funcional |
|---|---|---|
| `test_auth.py` | **8** | Login, renovación de refresh token y casos límite de credenciales erróneas. |
| `test_social_auth.py` | **15** | Integración simulada con Apple, Google y Facebook (nuevos registros, logins concurrentes, cuentas bloqueadas). |
| `test_users.py` | **17** | CRUD completo de usuarios, validación de campos con Pydantic, restricciones de entrada y carga de imágenes. |
| `test_excersices.py` | **8** | Listado de catálogos y filtros de exclusión inteligente de ejercicios basados en condiciones de salud del usuario. |
| `test_routines.py` | **3** | Comprobación del motor de rutinas con/sin perfil y exclusión de ejercicios prohibidos. |
| `test_unit.py` | **15** | Validación unitaria de expiración de tokens JWT, algoritmos de encriptación de contraseñas y mocks de API. |

---

## 📖 Resumen de Endpoints Principales (API v1)

Todos los endpoints están prefijados con `/api/v1`. Aquellos que requieren autenticación deben incluir el encabezado `Authorization: Bearer <JWT_ACCESS_TOKEN>`.

### 🔐 Autenticación tradicional y Social
- `POST /auth/login` — Autenticación básica y obtención de Access Token.
- `POST /auth/login/access-token` — Autenticación mediante OAuth2 Form.
- `POST /auth/refresh-token` — Renovación del token de acceso usando Refresh Token.
- `POST /auth/password-recovery/{email}` — Envío de correo electrónico para restablecer contraseña.
- `POST /auth/reset-password` — Restablecimiento seguro de contraseña con token.
- `POST /auth/social/{provider}` — Login/Registro con Redes Sociales (`apple`, `google`, `facebook`).

### 👤 Usuarios y Perfiles
- `POST /users/` — Registro de nuevo usuario básico.
- `GET /users/` — Listar todos los usuarios (requiere autenticación).
- `GET /users/me` — Obtener detalles del usuario autenticado.
- `GET /users/{id}` — Obtener datos de un usuario por ID.
- `PUT /users/{id}` — Actualizar perfil de usuario (solo el propietario).
- `POST /users/{id}/photo` — Subir y asociar imagen de perfil (solo el propietario).
- `DELETE /users/{id}` — Eliminar cuenta de usuario (solo el propietario).

### 🏋️ Catálogo Deportivo y Restricciones (Fase 6)
- `GET /excersices/levels` — Obtener catálogo de niveles de dificultad (`NIV1` a `NIV4`).
- `GET /excersices/goals` — Obtener catálogo de objetivos de entrenamiento (`PG`, `GMM`, etc.).
- `GET /excersices/conditions` — Obtener catálogo de condiciones médicas (con filtro `type` opcional para `PATHOLOGY` o `DISEASE`).
- `GET /excersices/methods` — Obtener catálogo de métodos de entrenamiento.
- `GET /excersices/` — Buscador y filtro de ejercicios. Permite enviar parámetros de exclusión (`exclude_conditions`) para descartar dinámicamente ejercicios no aptos por salud.

### 🤖 Generador de Rutinas Inteligentes (Fase 7)
- `POST /routines/generate` — Genera de manera automática una rutina personalizada para el usuario autenticado, combinando ejercicios viables filtrados por su equipamiento e historial médico, junto con las variables físicas (series, repeticiones, descanso y volumen) obtenidas de la matriz de programación.

### 💬 Inteligencia Artificial y Auditoría
- `POST /chat/completions` — Enviar un mensaje al asistente de IA (proxy OpenAI). Sujeto al límite global en Redis.
- `GET /prompt-logs/` — Dashboard del historial de prompts procesados por la IA. **Acceso exclusivo para administradores**.

---

## 🗄️ Comandos Útiles de Alembic (Migraciones)

```bash
# Crear nueva revisión de base de datos automáticamente basada en los modelos
alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar todas las migraciones pendientes hasta el último estado
alembic upgrade head

# Revertir la última migración aplicada
alembic downgrade -1

# Consultar la versión actual instalada en la base de datos
alembic current
```
