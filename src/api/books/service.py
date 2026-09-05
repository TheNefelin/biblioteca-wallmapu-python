from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.schemas.dtos import PaginationRequest, PaginationResponse
from src.schemas.dtos import BookRequest, BookResponse, BookDetailResponse
from src.schemas.dtos import GenreResponse, AuthorResponse, SubjectResponse
from src.api.book_authors import repository as book_authors_repository
from src.api.book_authors import service as book_author_service
from src.api.book_subjects import repository as book_subjects_repository
from src.api.book_subjects import service as book_subject_service
from src.api.reservations import repository as reservations_repository
from src.api.loans import repository as loans_repository
from . import repository


def _to_book_dto(item) -> BookResponse:
  """Convierte un objeto ORM Book a BookResponse, anidando relaciones como objetos."""
  return BookResponse(
    id_book=item.id_book,
    title=item.title,
    summary=item.summary,
    created_at=item.created_at,
    updated_at=item.updated_at,
    genre=GenreResponse.model_validate(item.genre),
    authors=[AuthorResponse.model_validate(ba.author) for ba in item.book_authors],
    subjects=[SubjectResponse.model_validate(bs.subject) for bs in item.book_subjects],
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse[list[BookDetailResponse]]:
  response = await repository.get_all_pagination(db, pagination)
  books = response.data or []
  data = [BookDetailResponse.model_validate(dict(row._mapping)) for row in books]

  return PaginationResponse[list[BookDetailResponse]](
    page=response.page,
    pages=response.pages,
    items=response.items,
    data=data,
    next=response.next,
    prev=response.prev,
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_book_by_id(db: AsyncSession, id: int) -> BookResponse | None:
  item = await repository.get_by_id(db, id)
  if not item:
    return None
  return _to_book_dto(item)


# -----------------------------------------------------------------
# CREATE
async def create_book(db: AsyncSession, data: BookRequest) -> BookResponse:
  dump = data.model_dump(exclude_unset=True)
  author_ids = dump.pop("author_ids", []) or []
  subject_ids = dump.pop("subject_ids", []) or []

  if dump.get("genre_id") == 0:
    raise BadRequestProblem(detail="El género es requerido")

  book = await repository.create(db, dump)
  await book_author_service.update_authors(db, book.id_book, author_ids)
  await book_subject_service.update_subjects(db, book.id_book, subject_ids)
  return _to_book_dto(await repository.get_by_id(db, book.id_book))


# -----------------------------------------------------------------
# UPDATE
async def update_book(db: AsyncSession, id: int, data: BookRequest) -> BookResponse | None:
  book = await repository.get_entity_by_id(db, id)
  if not book:
    return None

  dump = data.model_dump(exclude_unset=True)
  author_ids = dump.pop("author_ids", []) or []
  subject_ids = dump.pop("subject_ids", []) or []

  if dump.get("genre_id") == 0:
    raise BadRequestProblem(detail="El género es requerido")

  book = await repository.update(db, book, dump)
  await book_author_service.update_authors(db, book.id_book, author_ids)
  await book_subject_service.update_subjects(db, book.id_book, subject_ids)
  return _to_book_dto(await repository.get_by_id(db, book.id_book))


# -----------------------------------------------------------------
# DELETE
async def delete_book(db: AsyncSession, id: int) -> bool:
  book = await repository.get_entity_by_id(db, id)
  if not book:
    return False

  if await repository.has_authors(db, id):
    raise BadRequestProblem(detail="El libro tiene autores asociados")
  if await repository.has_subjects(db, id):
    raise BadRequestProblem(detail="El libro tiene descriptores asociados")
  if await repository.has_editions(db, id):
    raise BadRequestProblem(detail="El libro tiene ediciones/ejemplares asociados")

  dependencies = []

  active_reservations = await reservations_repository.get_active_by_book_id(db, id)
  if active_reservations:
    dependencies.append("reservas activas")

  active_loans = await loans_repository.get_active_by_book_id(db, id)
  if active_loans:
    dependencies.append("préstamos activos")

  if dependencies:
    raise BadRequestProblem(detail=f"No se puede eliminar el libro. Dependencias: {', '.join(dependencies)}")

  await book_authors_repository.delete_by_book(db, id)
  await book_subjects_repository.delete_by_book(db, id)
  await repository.delete(db, book)
  return True