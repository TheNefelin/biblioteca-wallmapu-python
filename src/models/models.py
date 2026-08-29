import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


# BIBLIOTECA ------------------------------------------------------
class Genre(Base):
  __tablename__ = "wm_genres"

  id_genre: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(200), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  books = relationship("Book", back_populates="genre")


class CopyStatus(Base):
  __tablename__ = "wm_copy_status"

  id_status: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(45), nullable=False)

  copies = relationship("Copy", back_populates="status")


class LoanStatus(Base):
  __tablename__ = "wm_loan_status"

  id_status: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(30), nullable=False)


class ReservationStatus(Base):
  __tablename__ = "wm_reservation_status"

  id_status: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(30), nullable=False)


class UserStatus(Base):
  __tablename__ = "wm_user_status"

  id_user_status: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(45), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  users = relationship("User", back_populates="user_status")


class UserRole(Base):
  __tablename__ = "wm_user_role"

  id_user_role: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(45), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  users = relationship("User", back_populates="user_role")


class Format(Base):
  __tablename__ = "wm_formats"

  id_format: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(200), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Editorial(Base):
  __tablename__ = "wm_editorials"

  id_editorial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(200), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  editions = relationship("Edition", back_populates="editorial")


class Author(Base):
  __tablename__ = "wm_authors"

  id_author: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(200), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  book_authors = relationship("BookAuthor", back_populates="author")


class Subject(Base):
  __tablename__ = "wm_subjects"

  id_subject: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(200), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  book_subjects = relationship("BookSubject", back_populates="subject")


class Region(Base):
  __tablename__ = "wm_regions"

  id_region: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  region: Mapped[str] = mapped_column(String(100), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  provinces = relationship("Province", back_populates="region")


class Province(Base):
  __tablename__ = "wm_provinces"

  id_province: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  province: Mapped[str] = mapped_column(String(100), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  region_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_regions.id_region"))

  region = relationship("Region", back_populates="provinces")
  communes = relationship("Commune", back_populates="province")


class Commune(Base):
  __tablename__ = "wm_communes"

  id_commune: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(45), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  province_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_provinces.id_province"))

  province = relationship("Province", back_populates="communes")
  users = relationship("User", back_populates="commune")


# NOTICIAS --------------------------------------------------------
class News(Base):
  __tablename__ = "wm_news"

  id_news: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String(45), nullable=False)
  subtitle: Mapped[str] = mapped_column(String(256), nullable=False)
  body: Mapped[str] = mapped_column(Text, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  images = relationship("NewsGallery", back_populates="news", order_by="NewsGallery.id_news_gallery")


class NewsGallery(Base):
  __tablename__ = "wm_news_gallery"

  id_news_gallery: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  alt: Mapped[str] = mapped_column(String(45), nullable=False)
  url: Mapped[str] = mapped_column(String(255), nullable=False)
  news_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_news.id_news"))

  news = relationship("News", back_populates="images")


# NÚCLEO DE NEGOCIO ----------------------------------------------
class Book(Base):
  __tablename__ = "wm_books"

  id_book: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String(200), nullable=False)
  summary: Mapped[str] = mapped_column(Text, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  genre_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_genres.id_genre"))
  genre = relationship("Genre", back_populates="books")

  book_authors = relationship("BookAuthor", back_populates="book")
  book_subjects = relationship("BookSubject", back_populates="book")
  editions = relationship("Edition", back_populates="book")

  @property
  def authors(self): return [ba.author for ba in self.book_authors]

  @property
  def subjects(self): return [bs.subject for bs in self.book_subjects]


class BookAuthor(Base):
  __tablename__ = "wm_book_author"

  id_book: Mapped[int] = mapped_column(Integer, ForeignKey("wm_books.id_book"), primary_key=True)
  id_author: Mapped[int] = mapped_column(Integer, ForeignKey("wm_authors.id_author"), primary_key=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  book = relationship("Book", back_populates="book_authors")
  author = relationship("Author", back_populates="book_authors")


class BookSubject(Base):
  __tablename__ = "wm_book_subject"

  id_book: Mapped[int] = mapped_column(Integer, ForeignKey("wm_books.id_book"), primary_key=True)
  id_subject: Mapped[int] = mapped_column(Integer, ForeignKey("wm_subjects.id_subject"), primary_key=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  book = relationship("Book", back_populates="book_subjects")
  subject = relationship("Subject", back_populates="book_subjects")


class Edition(Base):
  __tablename__ = "wm_editions"

  id_edition: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  edition: Mapped[str | None] = mapped_column(String(20), nullable=True)
  isbn: Mapped[str | None] = mapped_column(String(20), nullable=True)
  publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
  pages: Mapped[int] = mapped_column(Integer, nullable=False)
  cover_image: Mapped[str | None] = mapped_column(String(256), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  editorial_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_editorials.id_editorial"))
  editorial = relationship("Editorial", back_populates="editions")

  book_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_books.id_book"))
  book = relationship("Book", back_populates="editions")

  copies = relationship("Copy", back_populates="edition")
  edition_formats = relationship("EditionFormat", back_populates="edition")

  @property
  def formats(self): return [ef.format_rel for ef in self.edition_formats]


class EditionFormat(Base):
  __tablename__ = "wm_edition_format"

  id_edition: Mapped[int] = mapped_column(Integer, ForeignKey("wm_editions.id_edition"), primary_key=True)
  id_format: Mapped[int] = mapped_column(Integer, ForeignKey("wm_formats.id_format"), primary_key=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  edition = relationship("Edition", back_populates="edition_formats")
  format_rel = relationship("Format")


class Copy(Base):
  __tablename__ = "wm_copies"

  id_copy: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  signature_topography: Mapped[str] = mapped_column(String(100), nullable=False)
  copy_number: Mapped[int] = mapped_column(Integer, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  status_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_copy_status.id_status"))
  status = relationship("CopyStatus", back_populates="copies")

  edition_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_editions.id_edition"))
  edition = relationship("Edition", back_populates="copies")

  loans = relationship("Loan", back_populates="copy")
  reservations = relationship("Reservation", back_populates="copy")


class LoanPolicy(Base):
  __tablename__ = "wm_loan_policies"

  id_policy: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str | None] = mapped_column(String(100))
  max_books: Mapped[int | None] = mapped_column(Integer)
  max_days: Mapped[int | None] = mapped_column(Integer)
  reservation_days: Mapped[int | None] = mapped_column(Integer, default=3)


class User(Base):
  __tablename__ = "wm_users"

  id_user: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
  name: Mapped[str | None] = mapped_column(String(100))
  lastname: Mapped[str | None] = mapped_column(String(100))
  rut: Mapped[str | None] = mapped_column(String(12), unique=True)
  address: Mapped[str | None] = mapped_column(String(256))
  phone: Mapped[str | None] = mapped_column(String(10))
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  commune_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_communes.id_commune"))
  user_role_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_user_role.id_user_role"), default=3)
  user_status_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wm_user_status.id_user_status"), default=1)

  commune = relationship("Commune", back_populates="users")
  user_role = relationship("UserRole", back_populates="users")
  user_status = relationship("UserStatus", back_populates="users")
  reservations = relationship("Reservation", back_populates="user")


class Loan(Base):
  __tablename__ = "wm_loans"

  id_loan: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  loan_date: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
  due_date: Mapped[date] = mapped_column(Date, nullable=False)
  return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  copy_id: Mapped[int] = mapped_column(Integer, ForeignKey("wm_copies.id_copy"), nullable=False)
  copy = relationship("Copy", back_populates="loans")

  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wm_users.id_user"), nullable=False)
  user = relationship("User")

  loan_status_id: Mapped[int] = mapped_column(Integer, ForeignKey("wm_loan_status.id_status"), nullable=False, default=1)
  loan_status = relationship("LoanStatus")


class Reservation(Base):
  __tablename__ = "wm_reservations"

  id_reservation: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  reservation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wm_users.id_user"), nullable=False)
  user = relationship("User", back_populates="reservations")

  copy_id: Mapped[int] = mapped_column(Integer, ForeignKey("wm_copies.id_copy"), nullable=False)
  copy = relationship("Copy", back_populates="reservations")

  reservation_status_id: Mapped[int] = mapped_column(Integer, ForeignKey("wm_reservation_status.id_status"), nullable=False, default=1)
  status = relationship("ReservationStatus")


class Notification(Base):
  __tablename__ = "wm_notifications"

  id_notification: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  message: Mapped[str] = mapped_column(Text, nullable=False)
  is_priority: Mapped[bool] = mapped_column(Boolean, default=False)
  is_read: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wm_users.id_user"), nullable=False)
  user = relationship("User")
