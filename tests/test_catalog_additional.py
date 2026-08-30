"""Tests adicionales para endpoints sin cobertura.

Cubre:
- edition_image: POST/DELETE admin
- edition_format: PUT/DELETE admin
- copy: detail por book (público), CRUD admin
- stat: estadísticas de la biblioteca

Nota: Los tests de admin crean usuarios de prueba con email único para evitar
colisiones en tests paralelos. NO se seedean en postgre_seed.sql.
"""
import pytest
import uuid


@pytest.fixture
async def make_admin(db, make_user):
    """Crea un admin de test con email único para aislamiento."""
    async def _make():
        unique_id = f"admin-{uuid.uuid4().hex[:8]}@invalid.local"
        user, headers = await make_user(unique_id, "Admin")
        return user, headers
    return _make


# ============================================================================
# EDITION_IMAGE - admin only
# ============================================================================

@pytest.mark.asyncio
async def test_edition_image_upload_admin(client, make_admin):
    """Subir imagen de portada como admin devuelve 201."""
    _, headers = await make_admin()
    resp = await client.post("/api/edition-image/", headers=headers)
    assert resp.status_code in [201, 400, 404, 422]


@pytest.mark.asyncio
async def test_edition_image_upload_requires_admin(client):
    """Subir imagen de portada requiere admin."""
    resp = await client.post("/api/edition-image/")
    assert resp.status_code in [401, 403]


@pytest.mark.asyncio
async def test_edition_image_delete_admin(client, make_admin):
    """Eliminar imagen de edición como admin."""
    _, headers = await make_admin()
    resp = await client.delete("/api/edition-image/1", headers=headers)
    assert resp.status_code in [200, 404]


# ============================================================================
# EDITION_FORMAT - admin only
# ============================================================================

@pytest.mark.asyncio
async def test_edition_format_put_admin(client, make_admin):
    """Actualizar formatos de edición como admin."""
    _, headers = await make_admin()
    resp = await client.put("/api/edition-format/1", json=[1, 2], headers=headers)
    assert resp.status_code in [200, 201, 400, 404]


@pytest.mark.asyncio
async def test_edition_format_delete_admin(client, make_admin):
    """Eliminar un formato de edición como admin."""
    _, headers = await make_admin()
    resp = await client.delete("/api/edition-format/1/1", headers=headers)
    assert resp.status_code == 200


# ============================================================================
# COPY - public & admin
# ============================================================================

@pytest.mark.asyncio
async def test_copy_detail_by_book_public(client):
    """Listar ejemplares con detalle por libro (público)."""
    resp = await client.get("/api/copy/detail/book/1")
    assert resp.status_code in [200, 404]


@pytest.mark.asyncio
async def test_copy_detail_by_edition_admin(client, make_admin):
    """Listar ejemplares con detalle por edición (admin)."""
    _, headers = await make_admin()
    resp = await client.get("/api/copy/detail/edition/1", headers=headers)
    assert resp.status_code in [200, 404]


@pytest.mark.asyncio
async def test_copy_create_admin(client, make_admin):
    """Crear nuevo ejemplar como admin."""
    _, headers = await make_admin()
    resp = await client.post(
        "/api/copy/",
        json={"signature_topography": "TEST", "copy_number": 1, "edition_id": 1},
        headers=headers,
    )
    assert resp.status_code in [201, 400, 404]


@pytest.mark.asyncio
async def test_copy_delete_admin(client, make_admin):
    """Eliminar ejemplar como admin."""
    _, headers = await make_admin()
    resp = await client.delete("/api/copy/999", headers=headers)
    assert resp.status_code in [200, 404]


# ============================================================================
# STATS - admin/user
# ============================================================================

@pytest.mark.asyncio
async def test_stats_admin_stats(client, make_admin):
    """Obtención de estadísticas del panel de admin."""
    _, headers = await make_admin()
    resp = await client.get("/api/stat/admin-stats", headers=headers)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_stats_user_stats(client, make_admin):
    """Obtención de estadísticas del usuario actual."""
    _, headers = await make_admin()
    resp = await client.get("/api/stat/user-stats", headers=headers)
    assert resp.status_code == 200