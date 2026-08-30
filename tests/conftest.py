from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.core.config import settings
from src.core.database import get_db_async
from src.core.security import create_access_token as _create_token
from src.main import app
from src.models import models


BASE_DIR = Path(__file__).resolve().parent.parent
BASE_SQL_PATH = BASE_DIR / "postgre_base.sql"
SEED_SQL_PATH = BASE_DIR / "postgre_seed.sql"

test_db_url = settings.TEST_DATABASE_URL or settings.DATABASE_URL
engine = create_async_engine(test_db_url, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
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


@pytest.fixture
async def make_user(db):
  """Crea un usuario en la BD (misma sesión que el test) y devuelve (user, headers).
  role_name esperado: "Admin" o "Lector" (valores de wm_user_role).
  El token JWT es solo una pista; get_current_user lee el rol desde la BD."""
  async def _make(email, role_name="Lector", name="Test", user_role_id=None):
    role_id = user_role_id or (2 if role_name == "Admin" else 3)
    user = models.User(
      email=email,
      name=name,
      user_role_id=role_id,
      user_status_id=1,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user, ["user_role", "user_status"])
    headers = {"Authorization": f"Bearer {_create_token(user.id_user, role_name)}"}
    return user, headers
  return _make


@pytest.fixture
async def make_policy(db):
  """Crea (y realoja) una fila en wm_loan_policies para el test.
  Es una tabla de configuración, por lo que truncarla es seguro (aislamiento)."""
  async def _make(max_books=5, max_days=7, reservation_days=3, name="General"):
    await db.execute(text("TRUNCATE TABLE wm_loan_policies RESTART IDENTITY"))
    result = await db.execute(
      text(
        "INSERT INTO wm_loan_policies (name, max_books, max_days, reservation_days) "
        "VALUES (:n, :mb, :md, :rd) RETURNING id_policy"
      ),
      {"n": name, "mb": max_books, "md": max_days, "rd": reservation_days},
    )
    policy_id = result.scalar_one()
    await db.commit()
    return policy_id
  return _make
