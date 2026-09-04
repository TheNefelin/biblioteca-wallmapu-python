from datetime import date, datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID
import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


class AppModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)


# EDITORIALS ------------------------------------------------------
# Request: create/update comparten el mismo shape
class EditorialRequest(BaseModel):
  name: str


class EditorialResponse(AppModel):
  id_editorial: int
  name: str
  created_at: datetime
  updated_at: datetime


# GENRES ----------------------------------------------------------
# Request: create/update comparten el mismo shape
class GenreRequest(BaseModel):
  name: str = Field(..., description="Nombre del género")


class GenreResponse(AppModel, GenreRequest):
  id_genre: int
  created_at: datetime
  updated_at: datetime


# FORMAT ----------------------------------------------------------
# Request: create/update comparten el mismo shape
class FormatRequest(BaseModel):
  name: str


class FormatResponse(AppModel):
  id_format: int
  name: str
  created_at: datetime
  updated_at: datetime


# AUTHORS ---------------------------------------------------------
# Request: create/update comparten el mismo shape
class AuthorRequest(BaseModel):
  name: str


class AuthorResponse(AppModel):
  id_author: int
  name: str
  created_at: datetime
  updated_at: datetime

# SUBJECTS --------------------------------------------------------
# Request: create/update comparten el mismo shape
class SubjectRequest(BaseModel):
  name: str


class SubjectResponse(AppModel):
  id_subject: int
  name: str
  created_at: datetime
  updated_at: datetime


# CATÁLOGOS (solo lectura) ---------------------------------------
class CopyStatusResponse(AppModel):
  id_status: int
  name: str


class LoanStatusResponse(AppModel):
  id_status: int
  name: str


class ReservationStatusResponse(AppModel):
  id_status: int
  name: str


class UserStatusResponse(AppModel):
  id_user_status: int
  name: str
  created_at: datetime
  updated_at: datetime


class UserRoleResponse(AppModel):
  id_user_role: int
  name: str
  created_at: datetime
  updated_at: datetime


class RegionResponse(AppModel):
  id_region: int
  region: str
  created_at: datetime
  updated_at: datetime


class ProvinceResponse(AppModel):
  id_province: int
  province: str
  created_at: datetime
  updated_at: datetime
  region_id: int


class CommuneResponse(AppModel):
  id_commune: int
  name: str
  created_at: datetime
  updated_at: datetime
  province_id: int


# COPY ------------------------------------------------------------
# Request: create/update comparten el mismo shape
class CopyRequest(BaseModel):
  signature_topography: str
  edition_id: int
  copy_number: int
  status_id: int


class CopyResponse(AppModel, CopyRequest):
  status_name: str
  id_copy: int
  barcode: str
  created_at: datetime
  updated_at: datetime


class CopyDetailResponse(AppModel):
  id_copy: int
  barcode: str
  signature_topography: str
  copy_number: int
  created_at: datetime
  updated_at: datetime
  status_id: int
  status_name: str
  edition_id: int
  edition_name: str
  edition_isbn: Optional[str] = None
  edition_cover_image: Optional[str] = None
  editorial_id: int
  editorial_name: str
  is_availability: bool
  availability_status: str


# EDITION FORMAT --------------------------------------------------
class EditionFormatResponse(AppModel):
  id_edition: int
  id_format: int


# EDITIONS --------------------------------------------------------
# Base compartida por Request y Response
class BaseEdition(AppModel):
  edition: Optional[str] = None
  isbn: Optional[str] = None
  publication_year: int
  pages: int
  cover_image: Optional[str] = None
  editorial_id: int
  book_id: int


# Request: create/update (format_ids solo en creación)
class EditionRequest(BaseEdition):
  format_ids: Optional[list[int]] = None


class EditionResponse(BaseEdition):
  id_edition: int
  created_at: datetime
  updated_at: datetime
  formats: list[FormatResponse]


class EditionDetailResponse(BaseEdition):
  id_edition: int
  created_at: datetime
  updated_at: datetime
  editorial_name: str
  book_title: str
  genre_id: int
  genre_name: str
  author_id: Optional[int]
  author_name: Optional[str]
  copy_count: int


# Request: filtros de búsqueda para paginación
class EditionFilterRequest(BaseModel):
  id_author: Optional[int] = Field(None, description="Filtrar por autor")
  id_editorial: Optional[int] = Field(None, description="Filtrar por editorial")
  id_genre: Optional[int] = Field(None, description="Filtrar por género")
  id_format: Optional[int] = Field(None, description="Filtrar por formato")
  id_subject: Optional[int] = Field(None, description="Filtrar por descriptores")


# NEWS ------------------------------------------------------------
# Request: merge create + update
#   - Crear: title, subtitle, body (requeridos)
#   - Actualizar: id_news (requerido) + campos a modificar
class NewsRequest(BaseModel):
  id_news: Optional[int] = Field(None, description="ID de la noticia (requerido solo en actualización)")
  title: str = Field(..., description="Título de la noticia")
  subtitle: str = Field(..., description="Subtítulo de la noticia")
  body: str = Field(..., description="Cuerpo de la noticia")


class NewsResponse(AppModel):
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime


class NewsGalleryResponse(AppModel):
  id_news_gallery: int
  alt: str
  url: str
  news_id: int


class NewsWithGalleryResponse(AppModel):
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime
  images: list[NewsGalleryResponse]


# BOOK AUTHORS / BOOK SUBJECTS ------------------------------------
class BookAuthorResponse(AppModel):
  id_book: int
  id_author: int


class BookSubjectResponse(AppModel):
  id_book: int
  id_subject: int


# LOAN POLICIES ---------------------------------------------------
# Request: cuerpo de actualización (acepta id opcional para no romper el contrato del frontend)
class LoanPolicyRequest(AppModel):
  id_policy: Optional[int] = Field(None, description="Identificador de la política (opcional en el body)")
  name: Optional[str] = Field(None, description="Nombre de la política (ej: General, Estudiantes)")
  max_books: Optional[int] = Field(None, description="Cantidad máxima de libros que se pueden prestar")
  max_days: Optional[int] = Field(None, description="Número máximo de días de préstamo")
  reservation_days: Optional[int] = Field(3, description="Días que se mantiene una reserva activa")


# Response: salida de lectura
class LoanPolicyResponse(LoanPolicyRequest):
  id_policy: int = Field(..., description="Identificador único de la política de préstamo")


# LOANS -----------------------------------------------------------
# Request: solo create (no existe update de préstamo)
class LoanRequest(BaseModel):
  """Request para crear un nuevo préstamo"""
  copy_id: int = Field(..., description="ID del ejemplar a prestar")
  user_id: UUID = Field(..., description="UUID del usuario que toma el préstamo")


class LoanResponse(LoanRequest):
  """Response de préstamo con todos los campos"""
  id_loan: Optional[int] = Field(None, description="ID único del préstamo")
  loan_date: Optional[date] = Field(None, description="Fecha de creación del préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento del préstamo")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: Optional[int] = Field(None, description="ID del estado del préstamo (1=activo, 2=devuelto, 3=vencido)")
  created_at: Optional[datetime] = Field(None, description="Fecha de creación del registro en base de datos")
  updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización del registro")

  model_config = ConfigDict(from_attributes=True)


# Request: filtros de búsqueda para paginación
class LoanFilterRequest(BaseModel):
  """Request de filtros para paginación de préstamos"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=activo, 2=devuelto, 3=vencido)")


class LoanDetailResponse(AppModel):
  """Response plano para listados con datos esenciales de préstamo, usuario y libro"""
  id_loan: int = Field(..., description="ID único del préstamo")
  loan_date: date = Field(..., description="Fecha de creación del préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento del préstamo")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: int = Field(..., description="ID del estado del préstamo (1=activo, 2=devuelto, 3=vencido)")
  loan_status_name: str = Field(..., description="Nombre del estado del préstamo")
  user_id: UUID = Field(..., description="UUID del usuario que tiene el préstamo")
  user_name: str = Field(..., description="Nombre completo del usuario")
  copy_id: int = Field(..., description="ID del ejemplar prestado")
  copy_barcode: str = Field(..., description="Código de barras del ejemplar")
  copy_signature: str = Field(..., description="Signatura topográfica del ejemplar")
  book_id: int = Field(..., description="ID del libro al que pertenece el ejemplar")
  book_title: str = Field(..., description="Título del libro")


# RESERVATIONS ---------------------------------------------------
# Request: solo create (no existe update de reserva)
class ReservationRequest(BaseModel):
  """Request para crear una nueva reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a reservar")


class ReservationResponse(ReservationRequest):
  id_reservation: Optional[int] = None
  reservation_date: Optional[datetime] = None
  expiration_date: datetime
  user_id: UUID
  reservation_status_id: Optional[int] = None

  model_config = ConfigDict(from_attributes=True)


class ReservationDetailResponse(AppModel):
  """Response plano para listados con datos esenciales de reserva, usuario y libro"""
  id_reservation: int = Field(..., description="ID único de la reserva")
  reservation_date: datetime = Field(..., description="Fecha de creación de la reserva")
  expiration_date: datetime = Field(..., description="Fecha límite para retirar la reserva")
  user_id: UUID = Field(..., description="UUID del usuario que reserva")
  user_name: str = Field(..., description="Nombre del usuario")
  user_lastname: str = Field(..., description="Apellido del usuario")
  user_email: str = Field(..., description="Email del usuario")
  copy_id: int = Field(..., description="ID del ejemplar reservado")
  copy_barcode: str = Field(..., description="Código de barras del ejemplar")
  copy_signature: str = Field(..., description="Signatura topográfica del ejemplar")
  book_id: int = Field(..., description="ID del libro")
  book_title: str = Field(..., description="Título del libro")
  reservation_status_id: int = Field(..., description="ID del estado de la reserva")
  reservation_status_name: str = Field(..., description="Nombre del estado de la reserva")


# Request: acción de confirmar retiro
class ReservationPickupRequest(BaseModel):
  """Request para confirmar retiro de reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a entregar")


# Request: filtros de búsqueda para paginación
class ReservationFilterRequest(BaseModel):
  """Request de filtros para paginación de reservas"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=pendiente, 2=retirada, 3=cancelada, 4=vencida)")


# USERS -------------------------------------------------------------
# Request: merge create + update
#   - Crear: email (requerido), name (opcional)
#   - Actualizar: campos a modificar (todos opcionales)
class UserRequest(BaseModel):
  email: Optional[str] = Field(None, description="Correo electrónico (requerido en creación)")
  name: Optional[str] = Field(None, description="Nombre del usuario (puede no venir de Google)")
  lastname: Optional[str] = Field(None, description="Apellido del usuario")
  rut: Optional[str] = Field(None, description="RUT del usuario (formato 12345678-9)")
  address: Optional[str] = Field(None, description="Dirección del usuario")
  phone: Optional[str] = Field(None, description="Teléfono del usuario (máximo 10 dígitos)")
  commune_id: Optional[int] = Field(None, description="ID de la comuna")

  @field_validator('rut')
  @classmethod
  def validate_rut(cls, v):
    if v is None:
      return v
    if not re.match(r'^\d{7,8}-[\dkK]$', v):
      raise ValueError('RUT debe tener formato 12345678-9')
    return v

  @field_validator('phone')
  @classmethod
  def validate_phone(cls, v):
    if v is None:
      return v
    if not re.match(r'^\d{1,9}$', v):
      raise ValueError('Teléfono debe contener solo números (máximo 9 dígitos)')
    return v


# Request: extiende UserRequest con campos de admin
class UserAdminRequest(UserRequest):
  user_role_id: Optional[int] = Field(None, description="ID del rol del usuario")
  user_status_id: Optional[int] = Field(None, description="ID del estado del usuario")


class UserResponse(AppModel):
  id_user: UUID = Field(..., description="UUID único del usuario")
  email: str = Field(..., description="Correo electrónico del usuario")
  name: Optional[str] = Field(None, description="Nombre del usuario")
  lastname: Optional[str] = Field(None, description="Apellido del usuario")
  rut: Optional[str] = Field(None, description="RUT del usuario")
  address: Optional[str] = Field(None, description="Dirección del usuario")
  phone: Optional[str] = Field(None, description="Teléfono del usuario")
  created_at: datetime = Field(..., description="Fecha de creación del registro")
  updated_at: datetime = Field(..., description="Fecha de última actualización")
  commune_id: Optional[int] = Field(None, description="ID de la comuna")
  user_role_id: Optional[int] = Field(None, description="ID del rol del usuario")
  user_status_id: Optional[int] = Field(None, description="ID del estado del usuario")

  model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
  commune_name: Optional[str] = Field(None, description="Nombre de la comuna")
  user_role_name: Optional[str] = Field(None, description="Nombre del rol del usuario")
  user_status_name: Optional[str] = Field(None, description="Nombre del estado del usuario")


# NOTIFICATIONS --------------------------------------------------
# Request: merge create + update
#   - Crear: title, message, is_priority, user_id (requeridos)
#   - Actualizar (marcar leída): id_notification, is_read (requeridos)
class NotificationRequest(BaseModel):
  id_notification: Optional[int] = Field(None, description="ID de la notificación (requerido solo en actualización)")
  title: Optional[str] = Field(None, description="Título de la notificación (ej: 'PRÉSTAMO VENCIDO', 'ANUNCIO')")
  message: Optional[str] = Field(None, description="Mensaje detallado de la notificación")
  is_priority: Optional[bool] = Field(None, description="True = Alta prioridad (urgente), False = Normal")
  user_id: Optional[UUID] = Field(None, description="UUID del usuario destinatario")
  is_read: Optional[bool] = Field(None, description="Estado de lectura: True = Leída, False = No leída (requerido en actualización)")


class NotificationResponse(NotificationRequest):
  created_at: datetime = Field(..., description="Fecha de creación de la notificación")

  model_config = ConfigDict(from_attributes=True)


class NotificationDetailResponse(NotificationResponse):
  email: str = Field(..., description="Email del usuario destinatario")


# Request: filtros de búsqueda para paginación
class NotificationFilterRequest(BaseModel):
  is_read: bool = Field(default=True, description="filtrar (true = todos, false = solo no leidas)")


# Request: crear notificación por email (operación diferente a create/update)
class NotificationByEmailRequest(BaseModel):
  email: str = Field(..., description="Email del usuario destinatario")
  title: str = Field(..., description="Título de la notificación")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad, False = Normal")


# BOOKS -------------------------------------------------------------
# Request: merge create + update
#   - Crear: title, summary, genre_id, author_ids, subject_ids (requeridos)
#   - Actualizar: id_book (requerido) + campos a modificar
class BookRequest(BaseModel):
  id_book: Optional[int] = Field(None, description="ID del libro (requerido solo en actualización)")
  title: str
  summary: str
  genre_id: int
  author_ids: list[int]
  subject_ids: list[int]


class BookResponse(AppModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime
  genre: str = Field(..., description="Nombre del género")
  authors: list[str] = Field(..., description="Nombres de los autores")
  subjects: list[str] = Field(..., description="Nombres de los descriptores")

  model_config = ConfigDict(from_attributes=True)


class BookDetailResponse(AppModel):
  id_book: int
  title: str
  created_at: datetime
  updated_at: datetime
  genre_id: int
  genre_name: str
  author_id: Optional[int]
  author_name: Optional[str]
  edition_cover_image: Optional[str]
  edition_count: int
  copy_count: int

  model_config = ConfigDict(from_attributes=True)


# STATS -----------------------------------------------------------
class AdminStatsResponse(AppModel):
  reservations: int
  loans: int
  books: int
  users: int
  news: int


class UserStatsResponse(AppModel):
  total_borrowed: int
  active_loans: int
  overdue_loans: int


# AUTH --------------------------------------------------------------
class AuthUserResponse(AppModel):
  id_user: UUID
  email: EmailStr
  name: Optional[str] = None
  picture: Optional[str] = None
  profileComplete: bool
  role: str


class GoogleUserInfoResponse(AppModel):
  google_id: str
  email: str
  name: Optional[str] = None
  picture: Optional[str] = None
  email_verified: bool


class AuthGoogleRequest(BaseModel):
  googleToken: str


class AuthGoogleResponse(BaseModel):
  token: str
  user: AuthUserResponse


# PAGINACIÓN --------------------------------------------------------
T = TypeVar('T')

class PaginationRequest(BaseModel, Generic[T]):
  page: int = Field(default=1, ge=1, description="Número de página a mostrar")
  limit: int = Field(default=10, ge=1, le=100, description="Cantidad de elementos por página")
  search: Optional[str] = Field(default="", description="Texto de búsqueda opcional")
  filter: Optional[T] = Field(default=None, description="Filtros adicionales específicos del recurso")

class PaginationResponse(BaseModel, Generic[T]):
  page: int = Field(..., description="Página actual")
  pages: int = Field(..., description="Cantidad total de páginas disponibles")
  items: int = Field(..., description="Cantidad total de registros disponibles")
  next: Optional[str] = Field(None, description="URL de la siguiente página, si existe")
  prev: Optional[str] = Field(None, description="URL de la página anterior, si existe")
  data: Optional[T] = Field(None, description="Lista de resultados de la página actual")
