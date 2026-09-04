from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import BookAuthorResponse
from . import repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si author_ids viene vacÃ­o, elimina todas)
async def update_authors(db: AsyncSession, id_book: int, author_ids: list[int]) -> list[BookAuthorResponse]:
  author_ids = list(set(author_ids or []))
  items = await repository.update(db, id_book, author_ids)
  return [BookAuthorResponse.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relaciÃ³n book-author)
async def delete_author(db: AsyncSession, id_book: int, id_author: int) -> bool:
  return await repository.delete(db, id_book, id_author)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciÃ³nes book-author)
async def delete_author_by_book(db: AsyncSession, id_book: int) -> bool:
  return await repository.delete_by_book(db, id_book)