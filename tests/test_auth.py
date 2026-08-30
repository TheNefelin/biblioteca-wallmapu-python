"""Tests del servicio auth/get_or_create_user (flujo de login sin HTTP a Google)."""

from src.schemas.dtos import CreateUser
from src.api.users import service as user_service


async def test_get_or_create_user_creates_new(db):
  dto = CreateUser(email="nuevo@auth.cl", name="Nuevo")
  user = await user_service.get_or_create_user(db, dto)
  assert user is not None
  assert user.email == "nuevo@auth.cl"
  assert user.user_role_name == "Lector"


async def test_get_or_create_user_returns_existing(db, make_user):
  existing, _ = await make_user("existente@auth.cl", "Lector")
  dto = CreateUser(email="existente@auth.cl", name="Otro Nombre")
  user = await user_service.get_or_create_user(db, dto)
  assert user is not None
  assert user.email == "existente@auth.cl"
  assert user.id_user == existing.id_user


async def test_get_or_create_user_role_from_db(db, make_user):
  admin, _ = await make_user("admin@auth.cl", "Admin")
  dto = CreateUser(email="admin@auth.cl", name="Admin")
  user = await user_service.get_or_create_user(db, dto)
  assert user.user_role_name == "Admin"
