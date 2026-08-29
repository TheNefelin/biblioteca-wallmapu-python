from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import BookSubjectDTO
from . import repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, elimina todas)
async def update_subjects(db: AsyncSession, id_book: int, subject_ids: list[int]) -> list[BookSubjectDTO]:
  subject_ids = list(set(subject_ids or []))
  items = await repository.update(db, id_book, subject_ids)
  return [BookSubjectDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación book-subject)
async def delete_subject(db: AsyncSession, id_book: int, id_subject: int) -> bool:
  return await repository.delete(db, id_book, id_subject)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciónes book-subject)
async def delete_subject_by_book(db: AsyncSession, id_book: int) -> bool:
  return await repository.delete_by_book(db, id_book)