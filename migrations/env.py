from __future__ import with_statement
import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from api.models import Base

config = context.config

fileConfig(config.config_file_name)
logger = logging.getLogger('alembic')

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This mode is used when no database connection is available.
    The SQL is rendered as a script and is printed to the standard output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    In this mode, we connect to the database and run migrations.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
