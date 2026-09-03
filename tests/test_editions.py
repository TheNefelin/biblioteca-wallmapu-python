"""Tests de la feature editions (lectura pública + CRUD admin).

Reproduce y cubre la corrección del mapeo Row -> EditionDetailDTO en
get_all_pagination (dict(item._mapping)).
"""

import pytest


async def test_edition_pagination_public(client):
  """El endpoint público de paginación valida cada Row contra EditionDetailDTO."""
  resp = await client.get("/api/edition/pagination")
  assert resp.status_code == 200
  body = resp.json()
  assert body["page"] is not None
  assert isinstance(body["data"], list)
  assert len(body["data"]) > 0
  first = body["data"][0]
  assert "id_edition" in first
  assert "editorial_name" in first
  assert "book_title" in first


async def test_edition_by_book_public(client):
  resp = await client.get("/api/edition/book/1")
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)


async def test_edition_by_book_detail_requires_admin(client):
  """Detalle por book exige admin: sin token -> error."""
  resp = await client.get("/api/edition/book/1/detail")
  assert body_status_error(resp)


async def test_edition_by_book_detail_admin(client, make_user):
  admin, headers = await make_user("admin@ed3.cl", "Admin")
  resp = await client.get("/api/edition/book/1/detail", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert isinstance(body, list)


async def test_edition_pagination_requires_admin(client):
  """GET /api/edition/{id} (detail simple) exige admin: sin token -> 401."""
  resp = await client.get("/api/edition/1")
  assert body_status_error(resp)


async def test_edition_create_admin(client, make_user):
  admin, headers = await make_user("admin@ed.cl", "Admin")
  payload = {
    "edition": "Edición de prueba",
    "isbn": "9780000000001",
    "publication_year": 2024,
    "pages": 120,
    "editorial_id": 1,
    "book_id": 1,
    "format_ids": [1],
  }
  resp = await client.post("/api/edition/", json=payload, headers=headers)
  assert resp.status_code == 201
  body = resp.json()
  assert body is not None
  assert body["edition"] == "Edición de prueba"


async def test_edition_create_requires_admin(client):
  """Sin token, crear edición no debe estar permitido."""
  payload = {
    "edition": "X",
    "publication_year": 2024,
    "pages": 10,
    "editorial_id": 1,
    "book_id": 1,
  }
  resp = await client.post("/api/edition/", json=payload)
  assert body_status_error(resp)


async def test_edition_by_id_admin(client, make_user):
  admin, headers = await make_user("admin@ed2.cl", "Admin")
  resp = await client.get("/api/edition/1", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body is not None


async def test_edition_delete_blocked_by_formats(client, make_user):
  """Sin cascades: no se elimina una edición con formatos asociados (dependencia)."""
  admin, headers = await make_user("admin@ed4.cl", "Admin")
  payload = {
    "edition": "Edición con formato",
    "isbn": "9780000000002",
    "publication_year": 2024,
    "pages": 100,
    "editorial_id": 1,
    "book_id": 1,
    "format_ids": [1],
  }
  resp = await client.post("/api/edition/", json=payload, headers=headers)
  assert resp.status_code == 201
  edition_id = resp.json()["id_edition"]

  resp_del = await client.delete(f"/api/edition/{edition_id}", headers=headers)
  assert resp_del.status_code == 400
  assert "formatos asociados" in resp_del.json().get("detail", "")


async def test_edition_delete_ok_without_dependencies(client, make_user):
  """Se elimina una edición sin dependencias (sin copias ni formatos)."""
  admin, headers = await make_user("admin@ed5.cl", "Admin")
  payload = {
    "edition": "Edición sin dependencias",
    "isbn": "9780000000003",
    "publication_year": 2024,
    "pages": 90,
    "editorial_id": 1,
    "book_id": 1,
  }
  resp = await client.post("/api/edition/", json=payload, headers=headers)
  assert resp.status_code == 201
  edition_id = resp.json()["id_edition"]

  resp_del = await client.delete(f"/api/edition/{edition_id}", headers=headers)
  assert resp_del.status_code == 200
  assert resp_del.json() is True


def body_status_error(resp):
  """True si la API responde con un error RFC 9457 (auth/forbidden/servidor global)."""
  body = resp.json()
  return (
    not resp.is_success
    and "isSuccess" not in body
    and body.get("status") == resp.status_code
    and "detail" in body
    and "title" in body
  )
