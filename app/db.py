from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import urllib.parse

# Encode password safely
encoded_password = urllib.parse.quote_plus(settings.DATABASE_PASSWORD)

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DATABASE_USER}:{encoded_password}"
    f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
