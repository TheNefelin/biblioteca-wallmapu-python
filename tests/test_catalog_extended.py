"""Tests de lectura de catÃ¡logos de soporte (selecciÃ³n/selects).

Cubre los catÃ¡logos que no estaban incluidos en test_catalog_read.py:
- loan_status: GET pÃºblico (sin token).
- copy_status, reservation_status, division_commune/province/region,
  user_status, user_role: requieren auth ADMIN o LECTOR (se autentica un Lector).

Nota: estos endpoints responden ApiResponse (isSuccess + data).
"""


async def test_loan_status_public(client):
  resp = await client.get("/api/loan-status/")
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_copy_status_public(client, make_user):
  _, headers = await make_user("cs@cat.cl", "Lector")
  resp = await client.get("/api/copy-status/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_reservation_status_public(client, make_user):
  _, headers = await make_user("rs@cat.cl", "Lector")
  resp = await client.get("/api/reservation-status/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_division_region_public(client, make_user):
  _, headers = await make_user("dr@cat.cl", "Lector")
  resp = await client.get("/api/division-region/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_division_province_public(client, make_user):
  _, headers = await make_user("dp@cat.cl", "Lector")
  resp = await client.get("/api/division-province/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_division_commune_public(client, make_user):
  _, headers = await make_user("dc@cat.cl", "Lector")
  resp = await client.get("/api/division-commune/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_user_status_public(client, make_user):
  _, headers = await make_user("us@cat.cl", "Lector")
  resp = await client.get("/api/user-status/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


async def test_user_role_public(client, make_user):
  _, headers = await make_user("ur@cat.cl", "Lector")
  resp = await client.get("/api/user-role/", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)
  assert len(body) > 0


