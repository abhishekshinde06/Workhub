from logging.config import fileConfig
# Import every models.py so Base.metadata knows about all tables before
# autogenerate runs. Previously this only imported workhub.auth.models,
# which is why several past migrations in versions/ came out empty (the
# projects/task/etc. tables weren't registered on Base.metadata yet when
# `alembic revision --autogenerate` ran, so it had nothing to compare
# against and produced blank upgrade()/downgrade() functions).
from workhub.auth import models
from workhub.projects import models as project_models
from workhub.task import models as task_models
from workhub.comments import models as comment_models
from workhub.documents import models as document_models
from workhub.audit import models as audit_models
from workhub.chatbot import models as chatbot_models
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from workhub.db_connection import Base,engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
        In this scenario we need to create an Engine
        and associate a connection with the context.
    
        """
    with engine.connect() as connection:
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
