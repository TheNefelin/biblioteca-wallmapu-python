"""Tests de la feature loans: control de acceso y flujo de préstamo."""

from sqlalchemy import text


async def test_loan_pagination_requires_admin(client):
  resp = await client.get("/api/loans/pagination")
  body = resp.json()
  assert body["isSuccess"] is False


async def test_loan_pagination_admin(client, make_user):
  admin, headers = await make_user("admin@ln.cl", "Admin")
  resp = await client.get("/api/loans/pagination", headers=headers)
  assert resp.status_code == 200
  assert resp.json()["isSuccess"] is True


async def test_loan_create_requires_admin(client, make_policy):
  await make_policy()
  payload = {"copy_id": 1, "user_id": "00000000-0000-0000-0000-000000000000"}
  resp = await client.post("/api/loans/", json=payload)
  assert resp.json()["isSuccess"] is False


async def test_loan_create_without_policy_fails(client, db, make_user):
  # El seed siembra una política (Lectores); se trunca para garantizar el
  # escenario "sin política" (tabla de configuración aislada en db_testing).
  await db.execute(text("TRUNCATE TABLE wm_loan_policies RESTART IDENTITY"))
  await db.commit()
  admin, headers = await make_user("admin@ln2.cl", "Admin")
  lector, _ = await make_user("lector@ln2.cl", "Lector")
  payload = {"copy_id": 1, "user_id": str(lector.id_user)}
  resp = await client.post("/api/loans/", json=payload, headers=headers)
  body = resp.json()
  assert body["isSuccess"] is False


async def test_loan_create_and_return_admin(client, make_user, make_policy):
  await make_policy(max_days=7)
  admin, headers = await make_user("admin@ln3.cl", "Admin")
  lector, _ = await make_user("lector@ln3.cl", "Lector")

  payload = {"copy_id": 1, "user_id": str(lector.id_user)}
  resp = await client.post("/api/loans/", json=payload, headers=headers)
  assert resp.status_code == 201
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"]["copy_id"] == 1

  loan_id = body["data"]["id_loan"]
  resp = await client.put("/api/loans/copy/1/return", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"]["loan_status_id"] == 2
