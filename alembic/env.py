from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base  # Your SQLAlchemy models Base
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

# Alembic config object
config = context.config

# Logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = Base.metadata

# Get sync DB URL for Alembic (psycopg2)
def get_url():
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    db = os.getenv("DATABASE_NAME")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

# Offline migration (generates SQL file)
def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Online migration (executes SQL in DB)
def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": get_url()
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Choose mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
