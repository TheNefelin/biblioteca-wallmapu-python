"""Tests de la feature books (lectura pública + CRUD admin)."""


async def test_books_pagination_requires_admin(client):
  resp = await client.get("/api/books/pagination")
  assert resp.json()["isSuccess"] is False


async def test_books_pagination_admin(client, make_user):
  admin, headers = await make_user("admin@bk.cl", "Admin")
  resp = await client.get("/api/books/pagination", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert len(body["data"]["data"]) > 0


async def test_book_get_by_id_public(client):
  resp = await client.get("/api/books/1")
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"] is not None


async def test_book_create_requires_admin(client):
  payload = {"title": "X", "summary": "Y", "genre_id": 1, "author_ids": [1], "subject_ids": [1]}
  resp = await client.post("/api/books/", json=payload)
  assert resp.json()["isSuccess"] is False


async def test_book_create_update_delete_admin(client, make_user):
  admin, headers = await make_user("admin@bk2.cl", "Admin")

  payload = {"title": "Libro de test", "summary": "Resumen de test", "genre_id": 1, "author_ids": [], "subject_ids": []}
  resp = await client.post("/api/books/", json=payload, headers=headers)
  assert resp.status_code == 201
  body = resp.json()
  assert body["isSuccess"] is True
  book_id = body["data"]["id_book"]

  upd = {**payload, "id_book": book_id, "title": "Libro de test editado"}
  resp = await client.put(f"/api/books/{book_id}", json=upd, headers=headers)
  assert resp.status_code == 200
  assert resp.json()["data"]["title"] == "Libro de test editado"

  resp = await client.delete(f"/api/books/{book_id}", headers=headers)
  assert resp.status_code == 200
  assert resp.json()["isSuccess"] is True


async def test_book_delete_rejected_when_has_authors(client, make_user):
  """Regla de negocio: no se puede eliminar un libro con autores asociados."""
  admin, headers = await make_user("admin@bk3.cl", "Admin")
  payload = {"title": "Libro con autor", "summary": "S", "genre_id": 1, "author_ids": [1], "subject_ids": []}
  resp = await client.post("/api/books/", json=payload, headers=headers)
  assert resp.status_code == 201
  book_id = resp.json()["data"]["id_book"]

  resp = await client.delete(f"/api/books/{book_id}", headers=headers)
  body = resp.json()
  assert body["isSuccess"] is False
  assert "autor" in body["message"].lower()
