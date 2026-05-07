# Biblioteca Wallmapu API

API REST para la gestión de la Biblioteca Wallmapu, construida con FastAPI y PostgreSQL.

## Requisitos

- Python 3.12+
- PostgreSQL

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
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings
pip install python-jose[cryptography]
pip install pydantic[email]
pip install pillow
pip install python-multipart
pip install cloudinary
pip install sqlalchemy[asyncio]
pip install resend
```

```sh
pip freeze > requirements.txt
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env` basado en `.env_demo`:
```sh
cp .env_demo .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/biblioteca_wallmapu
SECRET_KEY=your-secret-key-here
CLOUDINARY_URL=cloudinary://...
```

### 4. Generar SECRET_KEY
```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Crear base de datos
```sh
psql -U postgres -c "CREATE DATABASE biblioteca_wallmapu;"
psql -U postgres -d biblioteca_wallmapu -f postgre.sql
```

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

---

## Estructura del Proyecto

```
biblioteca-wallmapu-python/
├── src/
│   ├── api/
│   │   ├── auth/
│   │   │   ├── routes.py
│   │   │   └── google_service.py
│   │   ├── authors/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── book_authors/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── book_subjects/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── books/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── copy/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── copy_status/
│   │   │   ├── dtos.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── division_communes/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── division_provinces/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── division_regions/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── edition_image/
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── editions/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── editorials/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── genres/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── loan_policies/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── loan_status/
│   │   │   ├── dtos.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── loans/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── news/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── news_gallery/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── notifications/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── reservation_status/
│   │   │   ├── dtos.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── reservations/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   ├── stats/
│   │   │   └── routes.py
│   │   ├── subjects/
│   │   │   ├── dtos.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   └── users/
│   │       ├── dtos.py
│   │       ├── models.py
│   │       ├── repository.py
│   │       ├── routes.py
│   │       └── service.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── jwt_service.py
│   │   ├── roles.py
│   │   └── url_helper.py
│   ├── services/
│   │   ├── cloudinary_service.py
│   │   └── image_service.py
│   ├── shared/
│   │   └── dtos.py
│   ├── __init__.py
│   └── main.py
├── static/
│   └── favicon.ico
├── .env
├── .env_demo
├── .gitignore
├── LICENSE.txt
├── postgre.sql
├── README.md
├── requirements.txt
├── run.py
└── vercel.json
```

---

## Roles de Usuario

| Rol | ID | Descripción |
|-----|-----|-------------|
| Super Admin | 1 | Acceso total al sistema |
| Admin | 2 | Gestión de recursos |
| Lector | 3 | Usuario regular |

---

## Endpoints Principales

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/auth/google` | Login con Google |
| POST | `/api/auth/register` | Registrar usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/auth/me` | Usuario actual |

### Gestión de Libros
| Recurso | Prefijo | Descripción |
|---------|---------|-------------|
| Books | `/api/books` | Gestión de libros |
| Editions | `/api/editions` | Ediciones de libros |
| Authors | `/api/authors` | Autores |
| Subjects | `/api/subjects` | Temas/Materias |
| Genres | `/api/genres` | Géneros literarios |
| Editorials | `/api/editorials` | Editoriales |

### Ejemplares
| Recurso | Prefijo | Descripción |
|---------|---------|-------------|
| Copies | `/api/edition-copy` | Ejemplares físicos |
| Copy Status | `/api/copy-status` | Estados de ejemplar |

### Préstamos y Reservas
| Recurso | Prefijo | Descripción |
|---------|---------|-------------|
| Reservations | `/api/reservations` | Reservas de libros |
| Reservation Status | `/api/reservation-status` | Estados de reserva |
| Loans | `/api/loans` | Préstamos activos |
| Loan Status | `/api/loan-status` | Estados de préstamo |
| Loan Policies | `/api/loan-policies` | Políticas de préstamo |
| Notifications | `/api/notifications` | Notificaciones |

### División Geográfica
| Recurso | Prefijo | Descripción |
|---------|---------|-------------|
| Regions | `/api/regions` | Regiones de Chile |
| Provinces | `/api/provinces` | Provincias |
| Communes | `/api/communes` | Comunas |

### Usuarios y Contenido
| Recurso | Prefijo | Descripción |
|---------|---------|-------------|
| Users | `/api/users` | Gestión de usuarios |
| User Role | `/api/user-role` | Roles de usuario |
| User Status | `/api/user-status` | Estados de usuario |
| News | `/api/news` | Noticias |
| Stats | `/api/stats` | Estadísticas |

---

## Flujo Reserva → Préstamo → Devolución

```
1. RESERVA (Usuario)
   POST /api/reservations
   - book_id: ID del libro
   - expiration_date: Fecha límite (3 días configurable)
   - status: Pendiente de retiro

2. RETIRO (Bibliotecario)
   PUT /api/reservations/{id}/pickup
   - Sistema busca ejemplar disponible
   - Crea préstamo automáticamente
   - Cambia estado a "Completada"

3. PRÉSTAMO
   - copy_id: Ejemplar asignado
   - due_date: Fecha de vencimiento
   - status: Activo

4. DEVOLUCIÓN (Bibliotecario)
   PUT /api/loans/{id}/return
   - return_date: Fecha de devolución
   - Ejemplar vuelve a estar disponible
   - status: Devuelto
```

### Estados de Reserva
| ID | Estado | Descripción |
|----|--------|-------------|
| 1 | Pendiente de retiro | Esperando que el usuario retire |
| 2 | Completada | Libro retirado |
| 3 | Cancelada | Reserva cancelada por usuario |
| 4 | Vencida | Pasó fecha límite sin retiro |

### Estados de Préstamo
| ID | Estado | Descripción |
|----|--------|-------------|
| 1 | Activo | En préstamo |
| 2 | Devuelto | Devuelto exitosamente |
| 3 | Vencido | Pasó fecha de vencimiento |

### Estados de Ejemplar
| ID | Estado | Descripción |
|----|--------|-------------|
| 1 | Disponible | Disponible para préstamo |
| 2 | Prestado | En préstamo activo |
| 3 | En reparación | En mantenimiento |
| 4 | Extraviado | No localizado |

---

## Autenticación

La API usa JWT para autenticación. Incluir en headers:
```
Authorization: Bearer <token>
```

### Roles en Endpoints
- **Todos**: Accessible sin autenticación
- **User/Admin**: Requiere token (Lector o Admin)
- **Admin**: Solo administradores

---

## Notas de Desarrollo

- La tabla `wm_news` contiene seed data de ejemplo (videojuegos/anime)
- Comunas, provincias y regiones están pre-cargadas para Chile
- Imágenes de portadas se almacenan en Cloudinary
- Sistema de reservas configurable (días de vigencia, máximo de libros, etc.)
