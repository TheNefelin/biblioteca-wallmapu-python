"""Tests de la feature users: control de acceso y CRUD con roles."""

import uuid


async def test_users_pagination_requires_admin(client):
  resp = await client.get("/api/users/pagination")
  body = resp.json()
  assert "isSuccess" not in body
  assert body["status"] == resp.status_code == 401
  assert "detail" in body


async def test_users_pagination_admin(client, make_user):
  admin, headers = await make_user("admin@us.cl", "Admin")
  lector, _ = await make_user("lector@us.cl", "Lector")
  resp = await client.get("/api/users/pagination", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body["data"], list)
  assert len(body["data"]) > 0


async def test_users_pagination_forbidden_for_lector(client, make_user):
  lector, headers = await make_user("lector@us2.cl", "Lector")
  resp = await client.get("/api/users/pagination", headers=headers)
  body = resp.json()
  assert "isSuccess" not in body
  assert body["status"] == resp.status_code == 403
  assert "detail" in body


async def test_user_get_by_id_requires_auth(client):
  resp = await client.get(f"/api/users/{uuid.uuid4()}")
  body = resp.json()
  assert "isSuccess" not in body
  assert body["status"] == resp.status_code == 401
  assert "detail" in body


async def test_user_get_by_id_admin(client, make_user):
  admin, headers = await make_user("admin@us3.cl", "Admin")
  lector, _ = await make_user("lector@us3.cl", "Lector")
  resp = await client.get(f"/api/users/{lector.id_user}", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["email"] == "lector@us3.cl"


async def test_user_update_own_profile(client, make_user):
  lector, headers = await make_user("lector@us4.cl", "Lector")
  payload = {
    "name": "Nuevo Nombre",
    "lastname": "Apellido",
    "rut": "12345678-9",
    "phone": "123456789",
  }
  resp = await client.put(f"/api/users/{lector.id_user}", json=payload, headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["name"] == "Nuevo Nombre"


async def test_user_update_not_allowed_other_user(client, make_user):
  user_a, headers_a = await make_user("user_a@us.cl", "Lector")
  user_b, _ = await make_user("user_b@us.cl", "Lector")
  payload = {"name": "Intruso"}
  resp = await client.put(f"/api/users/{user_b.id_user}", json=payload, headers=headers_a)
  body = resp.json()
  assert resp.status_code == 401
  assert body["status"] == 401
  assert "detail" in body


async def test_user_update_by_admin(client, make_user):
  admin, headers = await make_user("admin@us4.cl", "Admin")
  lector, _ = await make_user("lector@us5.cl", "Lector")
  payload = {"user_role_id": 2, "name": "Promovido"}
  resp = await client.put(f"/api/users/admin/{lector.id_user}", json=payload, headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["user_role_id"] == 2


async def test_user_update_by_admin_forbidden_for_lector(client, make_user):
  lector, headers = await make_user("lector@us6.cl", "Lector")
  admin, _ = await make_user("admin@usX.cl", "Admin")
  payload = {"name": "X"}
  resp = await client.put(f"/api/users/admin/{admin.id_user}", json=payload, headers=headers)
  body = resp.json()
  assert "isSuccess" not in body
  assert body["status"] == resp.status_code == 403
  assert "detail" in body
