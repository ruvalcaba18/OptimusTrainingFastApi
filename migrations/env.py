"""
Alembic environment configuration.

Cambios respecto al template por defecto:
  1. Lee SQLALCHEMY_DATABASE_URI desde el .env (via app.core.config.settings)
  2. Importa todos los modelos de app/models/ para que --autogenerate los detecte
  3. Inyecta la URL al config en tiempo de ejecución (nunca hardcodeada en alembic.ini)
"""
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ─── Asegurar que el root del proyecto esté en sys.path ─────────────────────
# Esto permite importar `app.*` desde cualquier lugar donde se corra alembic
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ─── Settings del proyecto (lee .env automáticamente) ──────────────────────
from app.core.config import settings  # noqa: E402

# ─── Importar Base y TODOS los modelos ──────────────────────────────────────
# IMPORTANTE: cada vez que agregues un nuevo modelo en app/models/,
# agrégalo aquí para que alembic --autogenerate lo detecte.
from app.database import Base  # noqa: E402
from app.models import User    # noqa: E402, F401

# Si en el futuro agregas más modelos, añádelos así:
# from app.models.sport import Sport        # noqa: F401
# from app.models.routine import Routine    # noqa: F401

# ─── Alembic config ──────────────────────────────────────────────────────────
config = context.config

# Inyectar la URL desde settings (sobreescribe el valor vacío de alembic.ini)
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de los modelos para autogenerate
target_metadata = Base.metadata


# ─── Modo OFFLINE ─────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """
    Corre migraciones sin conexión real — genera SQL puro.
    Útil para revisar el SQL antes de aplicarlo en producción.

    Uso:
        alembic upgrade head --sql > migration.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,      # Detecta cambios de tipo de columna
        compare_server_default=True,  # Detecta cambios en valores por defecto
    )
    with context.begin_transaction():
        context.run_migrations()


# ─── Modo ONLINE ──────────────────────────────────────────────────────────────
def run_migrations_online() -> None:
    """
    Corre migraciones con conexión real a la base de datos.
    Es el modo que se usa con: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Sin pool en migraciones (conexión única)
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,             # Detecta cambios de tipo de columna
            compare_server_default=True,   # Detecta cambios en DEFAULT
        )
        with context.begin_transaction():
            context.run_migrations()


# ─── Entry point ─────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
