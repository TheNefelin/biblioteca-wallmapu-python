from datetime import date, datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID
import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


class AppModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)


# GENRES ----------------------------------------------------------
class GenreRequest(BaseModel):
  name: str = Field(..., description="Nombre del género")


class GenreResponse(AppModel):
  id_genre: int
  name: str
  created_at: datetime
  updated_at: datetime


# CATÁLOGOS (solo lectura) ---------------------------------------
class CopyStatusDTO(AppModel):
  id_status: int
  name: str


class LoanStatusDTO(AppModel):
  id_status: int
  name: str


class ReservationStatusDTO(AppModel):
  id_status: int
  name: str


class UserStatusDTO(AppModel):
  id_user_status: int
  name: str
  created_at: datetime
  updated_at: datetime


class UserRoleDTO(AppModel):
  id_user_role: int
  name: str
  created_at: datetime
  updated_at: datetime


class RegionDTO(AppModel):
  id_region: int
  region: str
  created_at: datetime
  updated_at: datetime


class ProvinceDTO(AppModel):
  id_province: int
  province: str
  created_at: datetime
  updated_at: datetime
  region_id: int


class CommuneDTO(AppModel):
  id_commune: int
  name: str
  created_at: datetime
  updated_at: datetime
  province_id: int


# FORMAT ----------------------------------------------------------
class FormatRequest(BaseModel):
  name: str


class FormatResponse(AppModel):
  id_format: int
  name: str
  created_at: datetime
  updated_at: datetime


# EDITORIALS ------------------------------------------------------
class EditorialRequest(BaseModel):
  name: str


class EditorialResponse(AppModel):
  id_editorial: int
  name: str
  created_at: datetime
  updated_at: datetime


# AUTHORS ---------------------------------------------------------
class AuthorRequest(BaseModel):
  name: str


class AuthorResponse(AppModel):
  id_author: int
  name: str
  created_at: datetime
  updated_at: datetime


# SUBJECTS --------------------------------------------------------
class SubjectRequest(BaseModel):
  name: str


class SubjectResponse(AppModel):
  id_subject: int
  name: str
  created_at: datetime
  updated_at: datetime


# NEWS ------------------------------------------------------------
class CreateNewsDTO(BaseModel):
  title: str
  subtitle: str
  body: str


class UpdateNewsDTO(BaseModel):
  id_news: int
  title: str
  subtitle: str
  body: str


class NewsDTO(AppModel):
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime


class NewsGalleryDTO(AppModel):
  id_news_gallery: int
  alt: str
  url: str
  news_id: int


class NewsWithGalleryDTO(AppModel):
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime
  images: list[NewsGalleryDTO]


# BOOK AUTHORS / BOOK SUBJECTS ------------------------------------
class BookAuthorDTO(AppModel):
  id_book: int
  id_author: int


class BookSubjectDTO(AppModel):
  id_book: int
  id_subject: int


# LOAN POLICIES ---------------------------------------------------
class LoanPolicyDTO(BaseModel):
  id_policy: int = Field(..., description="Identificador único de la política de préstamo")
  name: Optional[str] = Field(None, description="Nombre de la política (ej: General, Estudiantes)")
  max_books: Optional[int] = Field(None, description="Cantidad máxima de libros que se pueden prestar")
  max_days: Optional[int] = Field(None, description="Número máximo de días de préstamo")
  reservation_days: Optional[int] = Field(3, description="Días que se mantiene una reserva activa")

  model_config = ConfigDict(from_attributes=True)


# EDITION FORMAT --------------------------------------------------
class EditionFormatDTO(AppModel):
  id_edition: int
  id_format: int


# EDITIONS --------------------------------------------------------
class CreateEditionDTO(BaseModel):
  edition: Optional[str] = None
  isbn: Optional[str] = None
  publication_year: int
  pages: int
  cover_image: Optional[str] = None
  editorial_id: int
  book_id: int
  format_ids: Optional[list[int]] = None


class UpdateEditionDTO(CreateEditionDTO):
  id_edition: int


class EditionDTO(AppModel):
  id_edition: int
  edition: Optional[str]
  isbn: Optional[str]
  publication_year: int
  pages: int
  cover_image: Optional[str]
  editorial_id: int
  book_id: int
  created_at: datetime
  updated_at: datetime
  formats: list[FormatResponse]


class EditionFilterDTO(BaseModel):
  id_author: Optional[int] = Field(None, description="Filtrar por autor")
  id_editorial: Optional[int] = Field(None, description="Filtrar por editorial")
  id_genre: Optional[int] = Field(None, description="Filtrar por género")
  id_format: Optional[int] = Field(None, description="Filtrar por formato")
  id_subject: Optional[int] = Field(None, description="Filtrar por descriptores")


class EditionDetailDTO(BaseModel):
  id_edition: int
  edition: Optional[str]
  isbn: Optional[str]
  publication_year: int
  pages: int
  cover_image: Optional[str]
  created_at: datetime
  updated_at: datetime
  editorial_id: int
  editorial_name: str
  book_id: int
  book_title: str
  genre_id: int
  genre_name: str
  author_id: Optional[int]
  author_name: Optional[str]
  copy_count: int


# LOANS -----------------------------------------------------------
class CreateLoanDTO(BaseModel):
  """DTO para crear un nuevo préstamo"""
  copy_id: int = Field(..., description="ID del ejemplar a prestar")
  user_id: UUID = Field(..., description="UUID del usuario que toma el préstamo")


class LoanDTO(CreateLoanDTO):
  """DTO de préstamo con todos los campos básicos"""
  id_loan: Optional[int] = Field(None, description="ID único del préstamo")
  loan_date: Optional[date] = Field(None, description="Fecha de creación del préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento del préstamo")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: Optional[int] = Field(None, description="ID del estado del préstamo (1=activo, 2=devuelto, 3=vencido)")
  created_at: Optional[datetime] = Field(None, description="Fecha de creación del registro en base de datos")
  updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización del registro")

  model_config = ConfigDict(from_attributes=True)


class LoanFilterDTO(BaseModel):
  """DTO de filtros para paginación de préstamos"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=activo, 2=devuelto, 3=vencido)")


class LoanDetailDTO(BaseModel):
  """DTO plano para listados con datos esenciales de préstamo, usuario y libro"""
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
class CreateReservationDTO(BaseModel):
  """DTO para crear una nueva reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a reservar")


class ReservationDTO(CreateReservationDTO):
  id_reservation: Optional[int] = None
  reservation_date: Optional[datetime] = None
  expiration_date: datetime
  user_id: UUID
  reservation_status_id: Optional[int] = None

  model_config = ConfigDict(from_attributes=True)


class ReservationDetailDTO(BaseModel):
  """DTO plano para listados con datos esenciales de reserva, usuario y libro"""
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


class ReservationPickupDTO(BaseModel):
  """DTO para confirmar retiro de reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a entregar")


class ReservationFilterDTO(BaseModel):
  """DTO de filtros para paginación de reservas"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=pendiente, 2=retirada, 3=cancelada, 4=vencida)")


# USERS -------------------------------------------------------------
class CreateUser(BaseModel):
  email: str = Field(..., description="Correo electrónico del usuario")
  name: Optional[str] = Field(None, description="Nombre del usuario (puede no venir de Google)")


class UpdateUserDTO(BaseModel):
  name: Optional[str] = Field(None, description="Nombre del usuario")
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


class UpdateUserByAdminDTO(UpdateUserDTO):
  user_role_id: Optional[int] = Field(None, description="ID del rol del usuario")
  user_status_id: Optional[int] = Field(None, description="ID del estado del usuario")


class UserDTO(BaseModel):
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


class UserDetailDTO(UserDTO):
  commune_name: Optional[str] = Field(None, description="Nombre de la comuna")
  user_role_name: Optional[str] = Field(None, description="Nombre del rol del usuario")
  user_status_name: Optional[str] = Field(None, description="Nombre del estado del usuario")


# NOTIFICATIONS --------------------------------------------------
class CreateNotificationDTO(BaseModel):
  title: str = Field(..., description="Título de la notificación (ej: 'PRÉSTAMO VENCIDO', 'ANUNCIO')")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad (urgente), False = Normal")
  user_id: UUID = Field(..., description="UUID del usuario destinatario")


class UpdateNotificationDTO(BaseModel):
  id_notification: int = Field(..., description="ID único de la notificación")
  is_read: bool = Field(..., description="Estado de lectura: True = Leída, False = No leída")


class NotificationDTO(CreateNotificationDTO, UpdateNotificationDTO):
  created_at: datetime = Field(..., description="Fecha de creación de la notificación")

  model_config = ConfigDict(from_attributes=True)


class NotificationDetailDTO(NotificationDTO):
  email: str = Field(..., description="Email del usuario destinatario")


class NotificationFilterDTO(BaseModel):
  is_read: bool = Field(default=True, description="filtrar (true = todos, false = solo no leidas)")


class CreateNotificationByEmailDTO(BaseModel):
  email: str = Field(..., description="Email del usuario destinatario")
  title: str = Field(..., description="Título de la notificación")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad, False = Normal")


# BOOKS -------------------------------------------------------------
class CreateBookDTO(BaseModel):
  title: str
  summary: str
  genre_id: int
  author_ids: list[int]
  subject_ids: list[int]


class UpdateBookDTO(CreateBookDTO):
  id_book: int


class BookDTO(BaseModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime
  genre: str = Field(..., description="Nombre del género")
  authors: list[str] = Field(..., description="Nombres de los autores")
  subjects: list[str] = Field(..., description="Nombres de los descriptores")

  model_config = ConfigDict(from_attributes=True)


class BookDetailDTO(BaseModel):
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


# COPY ------------------------------------------------------------
class SaveCopyDTO(BaseModel):
  signature_topography: str
  edition_id: int
  copy_number: int
  status_id: int


class CopyDTO(AppModel, SaveCopyDTO):
  status_name: str
  id_copy: int
  barcode: str
  created_at: datetime
  updated_at: datetime


class CopyDetailDTO(AppModel):
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


# STATS -----------------------------------------------------------
class AdminStatsDTO(BaseModel):
  reservations: int
  loans: int
  books: int
  users: int
  news: int


class UserStatsDTO(BaseModel):
  total_borrowed: int
  active_loans: int
  overdue_loans: int


# AUTH --------------------------------------------------------------
class AuthUser(BaseModel):
  id_user: UUID
  email: EmailStr
  name: Optional[str] = None
  picture: Optional[str] = None
  profileComplete: bool
  role: str


class GoogleUserInfo(BaseModel):
  google_id: str
  email: str
  name: Optional[str] = None
  picture: Optional[str] = None
  email_verified: bool


class AuthGoogleRequest(BaseModel):
  googleToken: str


class AuthGoogleResponse(BaseModel):
  token: str
  user: AuthUser


# COMPAT: nombres legacy reexportados por los features ------------
"""Estos alias se exponen desde los `dtos.py` de cada feature (compat
temporal) para no romper a los features aún síncronos que consumen los
nombres viejos. Se eliminarán al completar la migración."""


# PAGINACIÓN --------------------------------------------------------
T = TypeVar('T')

class PaginationRequestDTO(BaseModel, Generic[T]):
  page: int = Field(default=1, ge=1, description="Número de página a mostrar")
  limit: int = Field(default=10, ge=1, le=100, description="Cantidad de elementos por página")
  search: Optional[str] = Field(default="", description="Texto de búsqueda opcional")
  filter: Optional[T] = Field(default=None, description="Filtros adicionales específicos del recurso")

class PaginationResponseDTO(BaseModel, Generic[T]): 
  page: int = Field(..., description="Página actual")
  pages: int = Field(..., description="Cantidad total de páginas disponibles")
  items: int = Field(..., description="Cantidad total de registros disponibles")
  next: Optional[str] = Field(None, description="URL de la siguiente página, si existe")
  prev: Optional[str] = Field(None, description="URL de la página anterior, si existe")
  data: Optional[T] = Field(None, description="Lista de resultados de la página actual")


