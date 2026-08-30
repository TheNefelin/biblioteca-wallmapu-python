"""Tests de lectura de endpoints públicos del catálogo (sin autenticación).

Requieren BD de testing poblada con el MVP (fixture reset_mvp en conftest).
Solo ejercita endpoints GET que no dependen de token.
"""

import pytest


@pytest.mark.parametrize(
  "path,key",
  [
    ("/api/genre/", "genre"),
    ("/api/author/", "author"),
    ("/api/editorial/", "editorial"),
    ("/api/subject/", "subject"),
    ("/api/format/", "format"),
  ],
)
async def test_list_public_catalog(client, path, key):
  resp = await client.get(path)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert isinstance(body["data"], list)
  assert len(body["data"]) > 0
  assert "name" in body["data"][0]


async def test_news_list_paginated(client):
  resp = await client.get("/api/news/")
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  data = body["data"]
  assert data["page"] == 1
  assert isinstance(data["data"], list)
  assert len(data["data"]) > 0


async def test_get_editorial_by_id(client):
  resp = await client.get("/api/editorial/1")
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"] is not None
  assert body["data"]["id_editorial"] == 1


async def test_get_book_by_id(client):
  resp = await client.get("/api/books/1")
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"] is not None


async def test_get_news_by_id(client):
  resp = await client.get("/api/news/1")
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"] is not None
