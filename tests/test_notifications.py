"""Tests de la feature notifications: acceso, CRUD y marcado como leído."""

from src.models import models


async def test_notifications_pagination_requires_admin(client):
  resp = await client.get("/api/notifications/pagination")
  body = resp.json()
  assert body["isSuccess"] is False


async def test_notifications_pagination_admin(client, make_user, db):
  admin, headers = await make_user("admin@nt.cl", "Admin")
  db.add(models.Notification(user_id=admin.id_user, title="Anuncio", message="Mensaje 1", is_priority=False))
  await db.commit()
  resp = await client.get("/api/notifications/pagination", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True


async def test_notifications_user_pagination(client, make_user, db):
  lector, headers = await make_user("lector@nt.cl", "Lector")
  db.add(models.Notification(user_id=lector.id_user, title="Para mi", message="Hola", is_priority=False))
  await db.commit()
  resp = await client.get("/api/notifications/user/pagination", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert len(body["data"]["data"]) == 1


async def test_notifications_unread_count(client, make_user, db):
  lector, headers = await make_user("lector@nt2.cl", "Lector")
  db.add(models.Notification(user_id=lector.id_user, title="No leída", message="M", is_priority=False))
  await db.commit()
  resp = await client.get("/api/notifications/user/unread-count", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"] == 1


async def test_notifications_mark_as_read(client, make_user, db):
  lector, headers = await make_user("lector@nt3.cl", "Lector")
  notif = models.Notification(user_id=lector.id_user, title="Leer", message="M", is_priority=False)
  db.add(notif)
  await db.commit()
  await db.refresh(notif)
  resp = await client.put(f"/api/notifications/user/{notif.id_notification}/read", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  resp = await client.get("/api/notifications/user/unread-count", headers=headers)
  assert resp.json()["data"] == 0


async def test_notifications_mark_as_read_not_owner(client, make_user, db):
  owner, _ = await make_user("owner@nt.cl", "Lector")
  other, other_headers = await make_user("other@nt.cl", "Lector")
  notif = models.Notification(user_id=owner.id_user, title="Ajeno", message="M", is_priority=False)
  db.add(notif)
  await db.commit()
  await db.refresh(notif)
  resp = await client.put(f"/api/notifications/user/{notif.id_notification}/read", headers=other_headers)
  body = resp.json()
  assert body["isSuccess"] is False


async def test_notifications_create_admin(client, make_user):
  admin, headers = await make_user("admin@nt2.cl", "Admin")
  lector, _ = await make_user("lector@nt4.cl", "Lector")
  payload = {"email": "lector@nt4.cl", "title": "Anuncio", "message": "Bienvenido", "is_priority": False}
  resp = await client.post("/api/notifications", json=payload, headers=headers)
  assert resp.status_code == 201
  body = resp.json()
  assert body["isSuccess"] is True


async def test_notifications_get_by_id(client, make_user, db):
  lector, headers = await make_user("lector@nt5.cl", "Lector")
  notif = models.Notification(user_id=lector.id_user, title="Detalle", message="M", is_priority=False)
  db.add(notif)
  await db.commit()
  await db.refresh(notif)
  resp = await client.get(f"/api/notifications/{notif.id_notification}", headers=headers)
  assert resp.status_code == 200
  body = resp.json()
  assert body["isSuccess"] is True
  assert body["data"]["title"] == "Detalle"
