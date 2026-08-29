from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.core.config import settings


# ====================================================================#
# ENGINE ASYNC (asyncpg) - motor único desde la migración a async     #
# ====================================================================#
async_engine = create_async_engine(
  settings.DATABASE_URL,
  echo=settings.DEBUG,
  pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=async_engine,
  class_=AsyncSession,
)

# Base para modelos
Base = declarative_base()


# Dependencia asíncrona (todos los features migrados)
async def get_db_async():
  async with AsyncSessionLocal() as session:
    yield session