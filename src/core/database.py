from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# Engine de SQLAlchemy
engine = create_engine(
  settings.DATABASE_URL,
  echo=settings.DEBUG,  # ✅ Logs SQL en modo debug
  pool_pre_ping=True,   # ✅ Verificar conexión antes de usar
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