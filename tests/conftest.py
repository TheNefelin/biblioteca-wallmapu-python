from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.core.config import settings
from src.core.database import get_db_async
from src.main import app


BASE_DIR = Path(__file__).resolve().parent.parent
BASE_SQL_PATH = BASE_DIR / "postgre_base.sql"
SEED_SQL_PATH = BASE_DIR / "postgre_seed.sql"

test_db_url = settings.TEST_DATABASE_URL or settings.DATABASE_URL
engine = create_async_engine(test_db_url, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
  class_=AsyncSession,
)


def _split_sql(sql: str) -> list[str]:
  """Divide un script SQL por ';' respetando strings '...' (escape ''), '$$...$$' y comentarios '--'."""
  statements: list[str] = []
  current: list[str] = []
  i, n = 0, len(sql)
  in_string = False
  in_dollar = False

  while i < n:
    ch = sql[i]
    nxt = sql[i + 1] if i + 1 < n else ""

    if in_dollar:
      current.append(ch)
      if ch == "$" and nxt == "$":
        current.append(nxt)
        i += 2
        in_dollar = False
        continue
      i += 1
      continue

    if in_string:
      current.append(ch)
      if ch == "'" and nxt == "'":
        current.append(nxt)
        i += 2
        continue
      if ch == "'":
        in_string = False
      i += 1
      continue

    # Comentario de línea
    if ch == "-" and nxt == "-":
      while i < n and sql[i] != "\n":
        i += 1
      continue

    if ch == "'":
      in_string = True
      current.append(ch)
      i += 1
      continue

    if ch == "$" and nxt == "$":
      in_dollar = True
      current.append(ch)
      current.append(nxt)
      i += 2
      continue

    if ch == ";":
      stmt = "".join(current).strip()
      if stmt:
        statements.append(stmt)
      current = []
      i += 1
      continue

    current.append(ch)
    i += 1

  tail = "".join(current).strip()
  if tail:
    statements.append(tail)
  return statements


async def _run_script(conn, path: Path) -> None:
  """Ejecuta un script SQL statement por statement, omitiendo control transaccional/encoding."""
  sql = path.read_text(encoding="utf-8")
  for stmt in _split_sql(sql):
    lowered = stmt.lower()
    if lowered.startswith("begin") or lowered.startswith("commit"):
      continue
    if lowered.startswith("set "):
      continue
    await conn.execute(text(stmt + ";"))


@pytest.fixture
async def reset_mvp():
  """Recrea el esquema wm_* y lo puebla desde base+seed (restaurable)."""
  async with engine.begin() as conn:
    await _run_script(conn, BASE_SQL_PATH)
    await _run_script(conn, SEED_SQL_PATH)
  yield
  async with engine.begin() as conn:
    await _run_script(conn, BASE_SQL_PATH)
    await _run_script(conn, SEED_SQL_PATH)


@pytest.fixture
async def db(reset_mvp):
  async with TestingSessionLocal() as session:
    yield session


@pytest.fixture
async def client(db):
  async def override_get_db_async():
    yield db

  app.dependency_overrides[get_db_async] = override_get_db_async
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    yield ac
  app.dependency_overrides.clear()
