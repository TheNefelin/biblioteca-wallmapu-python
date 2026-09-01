"""Tests de la feature reservations: control de acceso y reglas de negocio."""


async def test_reservation_pagination_requires_admin(client):
  resp = await client.get("/api/reservations/pagination")
  body = resp.json()
  assert "isSuccess" not in body
  assert body["status"] == resp.status_code == 401
  assert "detail" in body


async def test_reservation_create_admin(client, make_user, make_policy):
  await make_policy(reservation_days=3)
  admin, headers = await make_user("admin@rs.cl", "Admin")
  resp = await client.post("/api/reservations/", json={"copy_id": 1}, headers=headers)
  assert resp.status_code == 201
  body = resp.json()
  assert body["copy_id"] == 1


async def test_reservation_create_not_available(client, make_user, make_policy):
  await make_policy()
  admin, headers = await make_user("admin@rs2.cl", "Admin")
  resp = await client.post("/api/reservations/", json={"copy_id": 10}, headers=headers)
  body = resp.json()
  assert resp.status_code in [400, 404]
  assert body["status"] == resp.status_code
  assert "detail" in body


async def test_reservation_create_duplicate_book(client, make_user, make_policy):
  await make_policy(max_books=5)
  admin, headers = await make_user("admin@rs3.cl", "Admin")
  resp = await client.post("/api/reservations/", json={"copy_id": 1}, headers=headers)
  assert resp.status_code == 201
  resp = await client.post("/api/reservations/", json={"copy_id": 2}, headers=headers)
  body = resp.json()
  assert resp.status_code == 400
  assert body["status"] == 400
  assert "detail" in body


async def test_reservation_cancel_owner(client, make_user, make_policy):
  await make_policy()
  lector, headers = await make_user("lector@rs.cl", "Lector")
  resp = await client.post("/api/reservations/", json={"copy_id": 1}, headers=headers)
  assert resp.status_code == 201
  reservation_id = resp.json()["id_reservation"]
  resp = await client.put(f"/api/reservations/{reservation_id}/cancel", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["reservation_status_id"] == 3


async def test_reservation_cancel_forbidden(client, make_user, make_policy):
  await make_policy()
  owner, owner_headers = await make_user("owner@rs.cl", "Lector")
  other, other_headers = await make_user("other@rs.cl", "Lector")
  resp = await client.post("/api/reservations/", json={"copy_id": 1}, headers=owner_headers)
  assert resp.status_code == 201
  reservation_id = resp.json()["id_reservation"]
  resp = await client.put(f"/api/reservations/{reservation_id}/cancel", headers=other_headers)
  body = resp.json()
  assert resp.status_code == 403
  assert body["status"] == 403
  assert "detail" in body


async def test_reservation_pickup_admin(client, make_user, make_policy):
  await make_policy(max_days=7, reservation_days=3)
  admin, headers = await make_user("admin@rs4.cl", "Admin")
  resp = await client.post("/api/reservations/", json={"copy_id": 1}, headers=headers)
  assert resp.status_code == 201
  reservation_id = resp.json()["id_reservation"]
  resp = await client.put(f"/api/reservations/{reservation_id}/pickup", json={"copy_id": 1}, headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["reservation_status_id"] == 2
