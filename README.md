# Biblioteca Wallmapu - API Python

Backend del proyecto Biblioteca Wallmapu desarrollado con Python 3.12 + FastAPI y PostgreSQL, siguiendo el patrón Senior.

---

## Requisitos

- Python 3.12+
- PostgreSQL
- [Brevo](https://www.brevo.com/es/)
- [Google Console](https://console.cloud.google.com/)
- [Cloudinary](https://console.cloudinary.com/)

---

## Instalación

### 1. Clonar y crear entorno virtual
```sh
git clone <repo-url>
cd biblioteca-wallmapu-python
py -m venv .venv
.venv\Scripts\activate
deactivate
```

### 2. Instalar dependencias
```sh
# Web framework y servidor
pip install fastapi uvicorn[standard]
# ORM y base de datos (async)
pip install sqlalchemy asyncpg greenlet
# Configuración y validación
pip install python-dotenv pydantic pydantic-settings
pip install pydantic[email]
# Autenticación JWT
pip install python-jose[cryptography]
# Rate limiting
pip install slowapi
# HTTP client (consumo de APIs externas: Google, Brevo)
pip install httpx
# Parseo de formularios multipart (subida de archivos)
pip install python-multipart
# Almacenamiento de imágenes en Cloudinary
pip install cloudinary
# Validación y procesamiento de imágenes
pip install pillow
# WebSocket (notificaciones en tiempo real)
pip install websockets
```
> **Nota:** `psycopg2-binary` fue reemplazado por `asyncpg` (driver async). `resend` dejó de usarse y `requests` ya no es dependencia: el envío de correos se hace vía **Brevo** con `httpx` async.

### 2.1 (Opcional) Dependencias de test
> Los tests ya están en uso (9 de catálogo en verde). Requieren una BD aislada conforme a `TEST_DATABASE_URL` (ver `.env_demo`).
```sh
pip install pytest pytest-asyncio
```

Guardar dependencias:
```sh
pip freeze > requirements.txt
```

Instalar desde requirements:
```sh
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env` basado en `.env_demo` (fuente de verdad de las variables requeridas):
```sh
cp .env_demo .env
```

Editar `.env` con tus credenciales reales. Ver el **formato y las variables requeridas** en `.env_demo`.

### 4. Generar SECRET_KEY
```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Crear base de datos
```sh
psql -U postgres -c "CREATE DATABASE biblioteca_wallmapu;"
psql -U postgres -d biblioteca_wallmapu -f postgre.sql
```

---

## Ejecutar

```sh
.venv\Scripts\activate
py run.py
```

O directamente:
```sh
uvicorn src.main:app --reload
```

**Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Tests
Los tests usan una BD aislada (`db_testing`) conforme a `TEST_DATABASE_URL` y restauran el esquema el patrón en cada corrida (solo tablas `wm_*`). Ejecutar con `run_test.py`:
```sh
.venv\Scripts\python.exe run_test.py
```
Definición: `tests/conftest.py` + `tests/test_catalog_read.py`. Base/seed: `postgre_base.sql` + `postgre_seed.sql`.

---

## Estructura del Proyecto

```
biblioteca-wallmapu-python/
├── src/
│   ├── api/                        # Módulos por dominio
│   │   ├── auth/                   # Autenticación JWT + Google
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── google_service.py
│   │   │
│   │   ├── authors/                # Autores (CRUD + Search)
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py       # Acceso a datos
│   │   │   ├── routes.py           # Endpoints
│   │   │   └── service.py          # Lógica de negocio
│   │   │
│   │   ├── book_authors/           # Relación libro-autor
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── book_subjects/          # Relación libro-materia
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── book_editorial/         # Editoriales
│   │   ├── book_genre/             # Géneros
│   │   ├── book_subject/           # Materias/Descriptores
│   │   │
│   │   ├── books/                  # Libros (CRUD + Paginación)
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── copy/                   # Ejemplares
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── copy_status/            # Estados de ejemplares
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── division_communes/      # Comunas
│   │   ├── division_provinces/     # Provincias
│   │   ├── division_regions/       # Regiones
│   │   │
│   │   ├── edition_image/          # Imágenes de ediciones
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── editions/                # Ediciones
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── editorials/             # Editoriales
│   │   ├── genres/                 # Géneros
│   │   │
│   │   ├── loan_policies/          # Políticas de préstamo
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── loan_status/            # Estados de préstamos
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── loans/                  # Préstamos
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── news/                   # Noticias
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── news_gallery/           # Galería de imágenes de noticias
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── notifications/          # Notificaciones in-app
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── connection_manager.py  # WebSocket
│   │   │
│   │   ├── reservation_status/     # Estados de reservas
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── reservations/           # Reservas
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── stats/                  # Estadísticas
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   ├── subjects/               # Materias
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   │
│   │   └── users/                  # Usuarios
│   │       ├── dtos.py
│   │       ├── models.py
│   │       ├── repository.py
│   │       ├── routes.py
│   │       ├── service.py
│   │       └── auth/
│   │           ├── routes.py
│   │           └── service.py
│   │
│   ├── core/                       # Configuración central
│   │   ├── config.py               # Settings (pydantic-settings)
│   │   ├── database.py             # async_engine + AsyncSession (asyncpg)
│   │   ├── security.py             # JWT + get_current_user (rol leído de la BD)
│   │   ├── dependencies.py         # require_admin / require_user
│   │   ├── limiter.py              # Rate limiting (slowapi)
│   │   ├── logger.py               # Logging JSON + request_id
│   │   ├── exceptions.py           # AppError y subclases
│   │   ├── roles.py                # Roles de usuario
│   │   ├── cloudinary.py           # Upload/delete de imágenes (Cloudinary)
│   │   ├── email.py                # Envío de emails (Brevo, httpx)
│   │   └── url_helper.py           # Helper para URLs
│   │
│   ├── models/                     # models.py centralizado (SQLAlchemy)
│   │
│   └── schemas/                    # DTOs y contratos de respuesta
│       └── dtos.py                 # ApiResponse, PaginationRequest/Response, DTOs
│
├── static/                         # Archivos estáticos
├── .env                            # Variables de entorno
├── .env_demo                       # Ejemplo de variables
├── postgre.sql                     # Schema de base de datos
├── requirements.txt                # Dependencias Python
├── run.py                          # Punto de entrada
└── main.py                         # FastAPI app
```

---

## Patrón Senior - Python FastAPI

### Arquitectura Repository → Service → Routes

```
Request → Routes → Service → Repository → Database
                    ↓
                  DTOs (validación)
```

### Reglas del Patrón Senior

**Repository:**
- `db` como 1er parámetro
- Sin try/catch (propaga excepciones)
- Retorna entidades SQLAlchemy, no DTOs

```python
# ✅ Correcto
def get_all(db: Session, pagination: PaginationRequestDTO):
    query = db.query(Loan).options(joinedload(Loan.user))
    return query.all()

# ❌ Incorrecto
def get_all(pagination, db: Session):  # db al final
    try:
        return db.query(Loan).all()
    except SQLAlchemyError as e:
        raise e  # Inútil, solo propaga
```

**Service:**
- Sin try/catch (propaga excepciones)
- Lógica de negocio aquí, no en repository
- Mapea entidades → DTOs

```python
# ✅ Correcto
def get_all_pagination(db: Session, pagination) -> PaginationResponseDTO:
    response = repository.get_all_pagination(db, pagination)
    items = [LoanDetailDTO.model_validate(i) for i in response.data]
    return PaginationResponseDTO(data=items, ...)
```

**Routes:**
- try/except con ApiResponse
- `db: Session = Depends(get_db)` como último parámetro
- summary/description en endpoints
- db primero al llamar service

```python
@router.get("/pagination", summary="Listar préstamos")
def get_loans(
    request: Request,
    pagination: PaginationRequestDTO = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return ApiResponse.success(service.get_all_pagination(db, pagination))
    except ValueError as e:
        return ApiResponse.bad_request(str(e))
    except Exception as e:
        return ApiResponse.server_error(str(e))
```

### DTOs con Pydantic

```python
class LoanDTO(BaseModel):
    id_loan: int
    loan_date: date
    due_date: date
    model_config = ConfigDict(from_attributes=True)

# Usar model_validate, no constructor directo
dto = LoanDTO.model_validate(loan_entity)
```

---

## Endpoints por Módulo

| Módulo | Prefijo | Roles |
|--------|---------|-------|
| Auth | `/api/auth` | Público |
| Books | `/api/books` | Admin |
| Editions | `/api/editions` | Admin/ Público (lectura) |
| Authors | `/api/authors` | Admin |
| Subjects | `/api/subjects` | Admin |
| Genres | `/api/genres` | Admin |
| Copy | `/api/edition-copy` | Admin |
| Loans | `/api/loans` | Admin / User |
| Reservations | `/api/reservations` | Admin / User |
| Notifications | `/api/notifications` | Admin / User |
| News | `/api/news` | Público (lectura) / Admin (escritura) |
| Users | `/api/users` | Admin |
| Stats | `/api/stats` | Admin / User |
| Divisiones | `/api/division-*` | Público |

---

## Flujo Reserva → Préstamo → Devolución

```
1. RESERVA (Usuario)
   POST /api/reservations
   → book_id, expiration_date

2. RETIRO (Admin - Two-Step Verification)
   PUT /api/reservations/{id}/pickup
   → Escanea reserva → Escanea libro físico → Confirma

3. PRÉSTAMO
   POST /api/loans
   → copy_id, user_id, due_date (calculado desde políticas)

4. DEVOLUCIÓN (Admin)
   PUT /api/loans/copy/{id}/return
   → Atualiza status del préstamo y del exemplar
```

---

## Estados

### Reserva
| ID | Estado |
|----|--------|
| 1 | Pendiente de retiro |
| 2 | Completada |
| 3 | Cancelada |
| 4 | Vencida |

### Préstamo
| ID | Estado |
|----|--------|
| 1 | Activo |
| 2 | Devuelto |
| 3 | Vencido |

### Ejemplar
| ID | Estado |
|----|--------|
| 1 | Disponible |
| 2 | Prestado |
| 3 | En reparación |
| 4 | Extraviado |

---

## Autenticación

JWT con headers:
```
Authorization: Bearer <token>
```

Roles: `ADMIN`, `LECTOR`

---

## Notas de Desarrollo

- Tabla `wm_news` contiene seed data de ejemplo
- Comunas, provincias y regiones pre-cargadas para Chile
- Imágenes almacenadas en Cloudinary
- Notificaciones in-app con WebSocket para tiempo real

---

*Documento basado en proyecto Biblioteca Wallmapu*
*Versión: Python 3.12 + FastAPI (2026)*