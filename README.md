# Optimus Training API 🚀

API robusta construida con **FastAPI** para la gestión de usuarios y entrenamientos, siguiendo las mejores prácticas de desarrollo y arquitectura de software.

## ✨ Características

- **Arquitectura Limpia**: Separación clara de responsabilidades (Servicios, Esquemas, Modelos, Rutas).
- **Persistencia con PostgreSQL**: Uso de SQLAlchemy ORM para una gestión de datos profesional.
- **Seguridad JWT**: Autenticación basada en JSON Web Tokens con expiración configurable.
- **Validación de Datos**: Validación estricta con Pydantic v2 (Emails, teléfonos, y tipos de entrenamiento específicos).
- **CRUD Completo**: Gestión total de perfiles de usuario.
- **Documentación Automática**: Swagger UI y ReDoc integrados.

## 🛠️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para base de datos.
- [PostgreSQL](https://www.postgresql.org/) - Sistema de base de datos relacional.
- [Pydantic v2](https://docs.pydantic.dev/) - Validación de datos.
- [Python-JOSE](https://python-jose.readthedocs.io/) - Gestión de JWT.
- [Passlib (bcrypt)](https://passlib.readthedocs.io/) - Hash de contraseñas.

## 🚀 Ejecución Local

### 1. Preparar la Base de Datos
Asegúrate de tener **PostgreSQL** instalado y crea una base de datos:
```sql
CREATE DATABASE optimus_db;
```

### 2. Configurar Entorno
Crea y activa tu entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 3. Variables de Entorno
Ajusta la URL de conexión en `app/core/config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://usuario:contraseña@localhost/optimus_db"
```

### 4. Iniciar el Servidor
```bash
uvicorn app.main:app --reload
```

---

## 📖 Especificaciones de la API

### Estructura de Esquemas
Los esquemas están modularizados en `app/schemas/users/` para facilitar el mantenimiento:
- `UserCreate`, `UserUpdate`, `UserResponse`, `UserLogin`, `Token`.

### Endpoints
- `POST /api/v1/login`: Inicia sesión y recibe un token.
- `POST /api/v1/users/`: Registro de nuevos usuarios.
- `GET /api/v1/users/me`: Perfil del usuario autenticado (Protegido).
- `PUT /api/v1/users/{id}`: Actualización persistente en DB (Protegido).

### Reglas de Validación
- **Teléfono**: Lógica de validación con Regex en `user_base.py`.
- **Entrenamiento**: Enum permitido: `casa`, `afuera`, `gimnasio`, `mixto`.

## 🧪 Documentación Interactiva
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
