import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.app.core.database import Base  # Import your SQLAlchemy models base
from src.app.core.config import settings  # Import your app settings
from src.app.models.auth import User
from src.app.models.cart import Cart
from src.app.models.record import Record

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        settings.DATABASE_URL,  # Используйте асинхронный URL из настроек
        poolclass=pool.NullPool,  # Опционально, рекомендуется для asyncio
    )

    async with connectable.connect() as connection:
        # Конфигурация через sync_connection
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,  # Для корректного сравнения типов
            )
        )

        # Выполнение миграций в синхронном контексте
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Запуск миграций."""
    with context.begin_transaction():
        context.run_migrations()




def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    In this scenario, we don't actually connect to the database, but
    just use the database URL directly from the configuration.

    """
    url = settings.DATABASE_URL # Use the async URL from settings
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
