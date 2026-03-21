# Biblioteca Wallmapu - Schema de Base de Datos

---

## API Endpoints

### `/api/auth` - Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| POST | `/register` | Registrar usuario | Público |
| POST | `/login` | Iniciar sesión | Público |
| GET | `/me` | Usuario actual | User/Admin |

---

### `/api/regions` - Regiones

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar regiones | Todos |
| GET | `/{id}` | Detalle de región | Todos |

---

### `/api/provinces` - Provincias

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar provincias | Todos |
| GET | `/{id}` | Detalle de provincia | Todos |
| GET | `/region/{region_id}` | Provincias por región | Todos |

---

### `/api/communes` - Comunas

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar comunas | Todos |
| GET | `/{id}` | Detalle de comuna | Todos |
| GET | `/province/{province_id}` | Comunas por provincia | Todos |

---

### `/api/user-role` - Roles de Usuario

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar roles | Todos |

---

### `/api/user-status` - Estados de Usuario

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar estados | Todos |

---

### `/api/users` - Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/detailed` | Listar usuarios (detallado) | Admin |
| GET | `/detailed/{id}` | Detalle de usuario | User/Admin |
| PUT | `/{id}` | Actualizar usuario | User |
| PUT | `/admin/{id}` | Actualizar usuario (Admin) | Admin |

---

### `/api/news` - Noticias

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar noticias | Todos |
| GET | `/{id}` | Detalle de noticia | Todos |
| POST | `/` | Crear noticia | Admin |
| PUT | `/{id}` | Actualizar noticia | Admin |
| DELETE | `/{id}` | Eliminar noticia | Admin |

---

### `/api/news-gallery` - Galería de Noticias

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/news/{news_id}` | Imágenes por noticia | Todos |
| POST | `/` | Crear imagen | Admin |
| DELETE | `/{id}` | Eliminar imagen | Admin |

---

### `/api/genres` - Géneros

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar géneros | Todos |

---

### `/api/authors` - Autores

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar autores | Todos |
| GET | `/{id}` | Detalle de autor | Todos |
| POST | `/` | Crear autor | Admin |
| PUT | `/{id}` | Actualizar autor | Admin |
| DELETE | `/{id}` | Eliminar autor | Admin |

---

### `/api/book-authors` - Relación Libro-Autor

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/book/{book_id}` | Autores por libro | Todos |
| POST | `/` | Asociar autor a libro | Admin |
| DELETE | `/{book_id}/{author_id}` | Desasociar autor | Admin |

---

### `/api/subjects` - Temas

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar temas | Todos |
| GET | `/{id}` | Detalle de tema | Todos |
| POST | `/` | Crear tema | Admin |
| PUT | `/{id}` | Actualizar tema | Admin |
| DELETE | `/{id}` | Eliminar tema | Admin |

---

### `/api/book-subjects` - Relación Libro-Tema

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/book/{book_id}` | Temas por libro | Todos |
| POST | `/` | Asociar tema a libro | Admin |
| DELETE | `/{book_id}/{subject_id}` | Desasociar tema | Admin |

---

### `/api/books` - Libros

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar libros (paginación) | Todos |
| GET | `/{id}` | Detalle de libro | Todos |
| POST | `/` | Crear libro | Admin |
| PUT | `/{id}` | Actualizar libro | Admin |
| DELETE | `/{id}` | Eliminar libro | Admin |

---

### `/api/editorials` - Editoriales

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar editoriales | Todos |
| GET | `/{id}` | Detalle de editorial | Todos |
| POST | `/` | Crear editorial | Admin |
| PUT | `/{id}` | Actualizar editorial | Admin |
| DELETE | `/{id}` | Eliminar editorial | Admin |

---

### `/api/editions` - Ediciones

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar ediciones | Todos |
| GET | `/{id}` | Detalle de edición | Todos |
| GET | `/book/{book_id}` | Ediciones por libro | Todos |
| GET | `/isbn/{isbn}` | Buscar por ISBN | Todos |
| POST | `/` | Crear edición | Admin |
| PUT | `/{id}` | Actualizar edición | Admin |
| DELETE | `/{id}` | Eliminar edición | Admin |

---

### `/api/edition-image` - Imagen de Edición

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| POST | `/{edition_id}` | Subir imagen de portada | Admin |

---

### `/api/edition-copy` - Ejemplares

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar ejemplares | User/Admin |
| GET | `/{id}` | Detalle de ejemplar | User/Admin |
| GET | `/edition/{id_edition}` | Ejemplares por edición | User/Admin |
| POST | `/` | Crear ejemplar | Admin |
| PUT | `/{id}` | Actualizar ejemplar | Admin |
| DELETE | `/{id}` | Eliminar ejemplar | Admin |

---

### `/api/copy-status` - Estados de Ejemplar

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar estados | Todos |

---

### `/api/reservation-status` - Estados de Reserva

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar estados | Todos |

---

### `/api/reservations` - Reservas

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar reservas | Admin |
| GET | `/user/{user_id}` | Reservas por usuario | User/Admin |
| GET | `/book/{book_id}` | Reservas activas por libro | Admin |
| GET | `/{id}` | Detalle de reserva | Todos |
| POST | `/` | Crear reserva | User/Admin |
| PUT | `/{id}/pickup` | Marcar como retirada | Admin |
| PUT | `/{id}/cancel` | Cancelar reserva | User/Admin |
| PUT | `/expire-overdue` | Marcar vencidas (batch) | Admin |
| DELETE | `/{id}` | Eliminar reserva | Admin |

---

### `/api/loan-status` - Estados de Préstamo

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar estados | Todos |

---

### `/api/loans` - Préstamos

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar préstamos | Admin |
| GET | `/user/{user_id}` | Préstamos por usuario | User/Admin |
| GET | `/book/{book_id}` | Préstamos por libro | Admin |
| GET | `/overdue` | Préstamos vencidos | Admin |
| GET | `/{id}` | Detalle de préstamo | Todos |
| POST | `/` | Crear préstamo | Admin |
| PUT | `/{id}/return` | Registrar devolución | Admin |
| PUT | `/mark-overdue` | Marcar vencidos (batch) | Admin |

---

### `/api/loan-policies` - Políticas de Préstamo

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar políticas | Admin |
| GET | `/{id}` | Detalle de política | Admin |
| POST | `/` | Crear política | Admin |
| PUT | `/{id}` | Actualizar política | Admin |
| DELETE | `/{id}` | Eliminar política | Admin |

---

### `/api/stats` - Estadísticas

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Estadísticas generales | Admin |

---

### `/api/notifications` - Notificaciones

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| GET | `/` | Listar notificaciones | Admin |
| GET | `/user/{user_id}` | Notificaciones por usuario | User/Admin |
| GET | `/user/{user_id}/unread` | Notificaciones no leídas | User/Admin |
| GET | `/{id}` | Detalle de notificación | Todos |
| POST | `/` | Crear notificación | Admin |
| PUT | `/{id}/read` | Marcar como leída | User/Admin |
| PUT | `/user/{user_id}/read-all` | Marcar todas como leídas | User/Admin |
| DELETE | `/{id}` | Eliminar notificación | Admin |
| DELETE | `/user/{user_id}` | Eliminar notificaciones de usuario | Admin |

---

## Índice de Tablas

| Tabla | Descripción |
|-------|-------------|
| [División Geográfica](#división-geográfica) | `wm_regions`, `wm_provinces`, `wm_communes` |
| [Usuarios](#usuarios) | `wm_users`, `wm_user_role`, `wm_user_status` |
| [Libros](#libros) | `wm_books`, `wm_editions`, `wm_copies` |
| [Autores y Temas](#autores-y-temas) | `wm_authors`, `wm_subjects`, `wm_genres` |
| [Relaciones Libros](#relaciones-libros) | `wm_book_author`, `wm_book_subject` |
| [Noticias](#noticias) | `wm_news`, `wm_news_gallery` |
| [Préstamos y Reservas](#préstamos-y-reservas) | `wm_reservations`, `wm_loans` |
| [Políticas y Estados](#políticas-y-estados) | `wm_loan_policies`, `wm_copy_status`, `wm_reservation_status` |
| [Notificaciones](#notificaciones) | `wm_notifications` |

---

## División Geográfica

### `wm_regions` - Regiones de Chile

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_region` | INTEGER | NO | PK, auto-increment |
| `region` | VARCHAR(100) | NO | Nombre de la región |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** 1:N con `wm_provinces`

---

### `wm_provinces` - Provincias

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_province` | INTEGER | NO | PK, auto-increment |
| `province` | VARCHAR(100) | NO | Nombre de la provincia |
| `region_id` | INTEGER | NO | FK → `wm_regions` |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_regions`, 1:N con `wm_communes`

---

### `wm_communes` - Comunas

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_commune` | INTEGER | NO | PK, auto-increment |
| `commune` | VARCHAR(100) | NO | Nombre de la comuna |
| `province_id` | INTEGER | SI | FK → `wm_provinces` |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_provinces`, 1:N con `wm_users`

---

## Usuarios

### `wm_user_role` - Roles de Usuario

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_user_role` | INTEGER | NO | PK, auto-increment |
| `role` | VARCHAR(45) | NO | Nombre del rol |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Valores por defecto:** Super Admin, Admin, Lector

---

### `wm_user_status` - Estados de Usuario

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_user_status` | INTEGER | NO | PK, auto-increment |
| `status` | VARCHAR(45) | NO | Estado del usuario |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Valores por defecto:** Activo/a, Deudor/a, Bloqueado/a

---

### `wm_users` - Usuarios

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_user` | UUID | NO | PK, UUID único |
| `email` | VARCHAR(100) | NO | Email único |
| `name` | VARCHAR(100) | SI | Nombre |
| `lastname` | VARCHAR(100) | SI | Apellido |
| `rut` | VARCHAR(12) | SI | RUT único |
| `address` | VARCHAR(256) | SI | Dirección |
| `phone` | VARCHAR(10) | SI | Teléfono |
| `commune_id` | INTEGER | SI | FK → `wm_communes` |
| `user_role_id` | INTEGER | NO | FK → `wm_user_role` (default: 3 - Lector) |
| `user_status_id` | INTEGER | NO | FK → `wm_user_status` (default: 1 - Activo) |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_communes`, N:1 con `wm_user_role`, N:1 con `wm_user_status`, 1:N con `wm_reservations`, 1:N con `wm_loans`, 1:N con `wm_notifications`

---

## Libros

### `wm_books` - Libros

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_book` | INTEGER | NO | PK, auto-increment |
| `title` | VARCHAR(200) | NO | Título del libro |
| `summary` | TEXT | SI | Resumen o descripción |
| `genre_id` | INTEGER | NO | FK → `wm_genres` |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_genres`, 1:N con `wm_editions`, 1:N con `wm_book_author`, 1:N con `wm_book_subject`, 1:N con `wm_reservations`

---

### `wm_genres` - Géneros Literarios

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_genre` | INTEGER | NO | PK, auto-increment |
| `name` | VARCHAR(200) | NO | Nombre del género |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Valores por defecto:** Novela, Cuento, Poesía, Ensayo, Teatro, Ciencia ficción, Fantasía, Terror, Misterio, Thriller, Romance, Aventura, Drama, Literatura infantil, Literatura juvenil, etc.

---

### `wm_editorials` - Editoriales

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_editorial` | INTEGER | NO | PK, auto-increment |
| `name` | VARCHAR(200) | NO | Nombre de la editorial |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

---

### `wm_editions` - Ediciones

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_edition` | INTEGER | NO | PK, auto-increment |
| `edition` | VARCHAR(50) | SI | Número/nombre de edición |
| `isbn` | VARCHAR(20) | NO | ISBN único |
| `publication_year` | INTEGER | NO | Año de publicación |
| `pages` | INTEGER | NO | Número de páginas |
| `cover_image` | VARCHAR(255) | SI | URL de imagen de portada |
| `book_id` | INTEGER | NO | FK → `wm_books` |
| `editorial_id` | INTEGER | NO | FK → `wm_editorials` |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_books`, N:1 con `wm_editorials`, 1:N con `wm_copies`

---

### `wm_copies` - Ejemplares

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_copy` | INTEGER | NO | PK, auto-increment |
| `barcode` | UUID | NO | Código de barras único |
| `signature_topography` | VARCHAR(100) | NO | Firma topográfica (ubicación física) |
| `copy_number` | VARCHAR(20) | NO | Número de ejemplar |
| `edition_id` | INTEGER | NO | FK → `wm_editions` |
| `status_id` | INTEGER | NO | FK → `wm_copy_status` (default: 1 - Disponible) |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** N:1 con `wm_editions`, N:1 con `wm_copy_status`, 1:N con `wm_loans`

---

## Autores y Temas

### `wm_authors` - Autores

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_author` | INTEGER | NO | PK, auto-increment |
| `name` | VARCHAR(200) | NO | Nombre del autor |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

---

### `wm_subjects` - Temas/Materias

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_subject` | INTEGER | NO | PK, auto-increment |
| `name` | VARCHAR(200) | NO | Nombre del tema |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

---

## Relaciones Libros

### `wm_book_author` - Relación Libro-Autor

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_book` | INTEGER | NO | FK → `wm_books` (parte de PK) |
| `id_author` | INTEGER | NO | FK → `wm_authors` (parte de PK) |
| `created_at` | TIMESTAMP | NO | Fecha de creación |

**PK Compuesta:** (`id_book`, `id_author`)

---

### `wm_book_subject` - Relación Libro-Tema

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_book` | INTEGER | NO | FK → `wm_books` (parte de PK) |
| `id_subject` | INTEGER | NO | FK → `wm_subjects` (parte de PK) |
| `created_at` | TIMESTAMP | NO | Fecha de creación |

**PK Compuesta:** (`id_book`, `id_subject`)

---

## Noticias

### `wm_news` - Noticias

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_news` | INTEGER | NO | PK, auto-increment |
| `title` | VARCHAR(100) | NO | Título |
| `subtitle` | VARCHAR(256) | NO | Subtítulo |
| `body` | TEXT | SI | Contenido |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Relaciones:** 1:N con `wm_news_gallery`

---

### `wm_news_gallery` - Galería de Noticias

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_news_gallery` | INTEGER | NO | PK, auto-increment |
| `alt` | VARCHAR(100) | NO | Texto alternativo de imagen |
| `url` | VARCHAR(256) | NO | URL de la imagen |
| `news_id` | INTEGER | SI | FK → `wm_news` |

**Relaciones:** N:1 con `wm_news`

---

## Préstamos y Reservas

### `wm_loan_status` - Estados de Préstamo

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_status` | INTEGER | NO | PK |
| `status` | VARCHAR(30) | NO | Nombre del estado |

**Valores:** Activo (1), Devuelto (2), Vencido (3)

---

### `wm_reservation_status` - Estados de Reserva

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_status` | INTEGER | NO | PK |
| `status` | VARCHAR(30) | NO | Nombre del estado |

**Valores:** Pendiente de retiro (1), Completada (2), Cancelada (3), Vencida (4)

---

### `wm_reservations` - Reservas

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_reservation` | INTEGER | NO | PK, auto-increment |
| `reservation_date` | TIMESTAMP | NO | Fecha de reserva (default: ahora) |
| `expiration_date` | TIMESTAMP | NO | Fecha de expiración |
| `user_id` | UUID | NO | FK → `wm_users` |
| `book_id` | INTEGER | NO | FK → `wm_books` |
| `reservation_status_id` | INTEGER | NO | FK → `wm_reservation_status` (default: 1) |

**Relaciones:** N:1 con `wm_users`, N:1 con `wm_books`, N:1 con `wm_reservation_status`

**Flujo:** pending_pickup → completed (al retirar) | cancelled (cancelada) | expired (vencida)

---

### `wm_loans` - Préstamos

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_loan` | INTEGER | NO | PK, auto-increment |
| `loan_date` | DATE | NO | Fecha de préstamo (default: hoy) |
| `due_date` | DATE | NO | Fecha de vencimiento |
| `return_date` | DATE | SI | Fecha de devolución |
| `copy_id` | INTEGER | NO | FK → `wm_copies` |
| `user_id` | UUID | NO | FK → `wm_users` |
| `loan_status_id` | INTEGER | NO | FK → `wm_loan_status` (default: 1) |
| `created_at` | TIMESTAMP | NO | Fecha de creación |
| `updated_at` | TIMESTAMP | NO | Fecha de actualización |

**Estados:** Activo (1), Devuelto (2), Vencido (3)

**Relaciones:** N:1 con `wm_copies`, N:1 con `wm_users`, N:1 con `wm_loan_status`

---

## Políticas y Estados

### `wm_loan_policies` - Políticas de Préstamo

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_policy` | INTEGER | NO | PK, auto-increment |
| `name` | VARCHAR(100) | SI | Nombre de la política |
| `max_books` | INTEGER | SI | Máximo de libros por usuario |
| `max_days` | INTEGER | SI | Máximo de días de préstamo |
| `fine_per_day` | DECIMAL(10,2) | SI | Multa por día de atraso |
| `reservation_days` | INTEGER | NO | Días de vigencia de reserva (default: 3) |

---

### `wm_copy_status` - Estados de Ejemplar

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_status` | SMALLINT | NO | PK |
| `name` | VARCHAR(30) | NO | Nombre del estado |

**Valores:** Disponible (1), Prestado (2), En reparación (3), Extraviado (4)

---

## Notificaciones

### `wm_notifications` - Notificaciones

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id_notification` | INTEGER | NO | PK, auto-increment |
| `title` | VARCHAR(100) | NO | Título |
| `message` | TEXT | NO | Mensaje |
| `is_read` | BOOLEAN | NO | ¿Leída? (default: FALSE) |
| `user_id` | UUID | NO | FK → `wm_users` |
| `created_at` | TIMESTAMP | NO | Fecha de creación |

**Relaciones:** N:1 con `wm_users`

---

## Diagrama de Relaciones

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USUARIOS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  wm_users ────────┬───→ wm_user_role                                         │
│                  ├───→ wm_user_status                                       │
│                  └───→ wm_communes ────→ wm_provinces ────→ wm_regions     │
└──────────────────┬────────────────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌─────────────────┐
│ wm_reservations│    │   wm_loans      │
├───────────────┤    ├─────────────────┤
│ book_id ──────┼───→│ wm_books        │
│ user_id ──────┼───→│ copy_id ────────┼──→ wm_copies
│ status ────────┼───→│ user_id         │              │
└───────────────┘    └────────┬─────────┘              │
                             │                        │
                             ▼                        ▼
                     ┌───────────────┐        ┌──────────────┐
                     │   wm_fines    │        │ wm_copy_status
                     └───────────────┘        └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              LIBROS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  wm_books ───────→ wm_genres                                                │
│       │                                                                      │
│       ├───→ wm_editions ───→ wm_editorials                                 │
│       │              │                                                       │
│       └───→ wm_copies ────→ wm_copy_status                                 │
│                                                                            │
│  wm_books ───────→ wm_book_author ───→ wm_authors                          │
│  wm_books ───────→ wm_book_subject ───→ wm_subjects                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo Reserva → Préstamo → Devolución

```
1. RESERVA                    2. RETIRO                    3. PRÉSTAMO
   (Usuario)                    (Bibliotecario)              (Sistema)
   
   book_id                  Verificar reserva          Asignar copy_id
   user_id                  Buscar copia               loan_date = hoy
   expiration_date          disponible                 due_date = hoy + max_days
   status = pending_pickup  Marcar pickup             status = active
                                                           copy.status = Prestado
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │       NOTIFICACIÓN           │
                     │  "Libro listo para retiro"  │
                     └──────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
   ┌───────────┐            ┌───────────┐            ┌───────────┐
   │ COMPLETED │            │ CANCELLED │            │  EXPIRED │
   │  (2)      │            │   (3)    │            │   (4)    │
   └───────────┘            └───────────┘            └───────────┘
   
                                  4. DEVOLUCIÓN
                                     (Bibliotecario)
                                     
                                  return_date = hoy
                                  status = returned
                                  copy.status = Disponible
                                  
                                  ┌───────────────┐
                                  │ Si vencida:   │
                                  │ Generar multa │
                                  │ (wm_fines)    │
                                  └───────────────┘
```

---

## Índices Creados

| Índice | Tabla | Campo |
|--------|-------|-------|
| `idx_edition_isbn` | `wm_editions` | `isbn` |
| `idx_book_title` | `wm_books` | `title` |
| `idx_book_summary` | `wm_books` | `summary` |
| `idx_book_genre` | `wm_books` | `genre_id` |
| `idx_author_id` | `wm_book_author` | `id_author` |
| `idx_editorial_id` | `wm_editions` | `editorial_id` |
