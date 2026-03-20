from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from src.core.config import settings

# Engine de SQLAlchemy
engine = create_engine(
  settings.DATABASE_URL,
  echo=settings.DEBUG,
  pool_pre_ping=True,
  poolclass=QueuePool,
  pool_size=10,
  max_overflow=20,
  pool_recycle=3600,
  pool_timeout=30,
  connect_args={
    "connect_timeout": 10,
    "options": "-c statement_timeout=30000",
  },
)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()