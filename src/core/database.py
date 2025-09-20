from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

# Создаём движок
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# Фабрика сессий
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
