"""Tests de la entidad format con el contrato nuevo (sin ApiResponse / RFC 9457).

Verifica que /api/format/* devuelve respuestas CRUDAS (modelo o ErrorDetail
RFC 9457) sin el envelope ApiResponse, replicando el patrón de la referencia.

Seguridad: usa la BD aislada `db_testing` vía la fixture `reset_mvp`, que
restaura el esquema+seed de las tablas `wm_*` al inicio y al teardown de cada
test. Los formatos creados aquí usan nombre único y son limpiados por el
teardown; nunca se borran filas del seed fuera del test.
"""
import pytest
import uuid

PROTECTED_RESPONSES = [401, 403]


@pytest.fixture
async def make_admin(db, make_user):
    """Crea un admin de test con email único para aislamiento."""
    async def _make():
        unique_id = f"admin-{uuid.uuid4().hex[:8]}@invalid.local"
        user, headers = await make_user(unique_id, "Admin")
        return user, headers
    return _make


# ============================================================================
# GET ALL (público) - lista cruda
# ============================================================================

@pytest.mark.asyncio
async def test_format_get_all_public_crudo(client):
    """GET /api/format/ devuelve una lista cruda (sin isSuccess)."""
    resp = await client.get("/api/format/")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "name" in body[0]


# ============================================================================
# GET ALL PAGINATION (admin) - paginación cruda
# ============================================================================

@pytest.mark.asyncio
async def test_format_pagination_admin_crudo(client, make_admin):
    """GET /api/format/pagination devuelve paginación cruda (sin isSuccess)."""
    _, headers = await make_admin()
    resp = await client.get("/api/format/pagination?page=1&limit=5", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["page"] == 1
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0
    assert "name" in body["data"][0]
    assert "isSuccess" not in body


@pytest.mark.asyncio
async def test_format_pagination_requires_admin(client):
    """GET /api/format/pagination sin token devuelve error RFC 9457 (no ApiResponse)."""
    resp = await client.get("/api/format/pagination?page=1&limit=5")
    assert resp.status_code in PROTECTED_RESPONSES
    assert "isSuccess" not in resp.json()


# ============================================================================
# CRUD (admin) - respuestas crudas
# ============================================================================

@pytest.mark.asyncio
async def test_format_create_update_delete_crudo(client, make_admin):
    """Create/update/delete devuelven el modelo o booleano crudo (sin ApiResponse)."""
    _, headers = await make_admin()
    name = f"Formato Test {uuid.uuid4().hex[:8]}"

    # CREATE -> 201 + FormatResponse crudo
    resp = await client.post("/api/format/", json={"name": name}, headers=headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == name
    assert "id_format" in body
    assert "isSuccess" not in body
    fmt_id = body["id_format"]

    # UPDATE -> 200 + FormatResponse crudo
    new_name = f"{name} actualizado"
    resp = await client.put(f"/api/format/{fmt_id}", json={"name": new_name}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == new_name
    assert body["id_format"] == fmt_id
    assert "isSuccess" not in body

    # DELETE -> 200 + bool crudo
    resp = await client.delete(f"/api/format/{fmt_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json() is True


@pytest.mark.asyncio
async def test_format_duplicate_error_is_problem_plus_json(client, make_admin):
    """Crear un formato con nombre duplicado devuelve 400 con 'detail' (RFC 9457)."""
    _, headers = await make_admin()
    resp = await client.post("/api/format/", json={"name": "Sin Clasificar"}, headers=headers)
    assert resp.status_code == 400
    body = resp.json()
    assert "isSuccess" not in body
    assert "detail" in body
    assert body["status"] == 400
