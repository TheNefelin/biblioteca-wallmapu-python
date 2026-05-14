from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si author_ids viene vacío, elimina todas)
def update_authors(db: Session, id_book: int, author_ids: list[int]) -> list[dtos.BookAuthorDTO]:
  author_ids = list(set(author_ids or []))
  items = repository.update(db, id_book, author_ids)
  return [dtos.BookAuthorDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación book-author)
def delete_author(db: Session, id_book: int, id_author: int) -> bool:
  return repository.delete(db, id_book, id_author)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciónes book-author)
def delete_author_by_book(db: Session, id_book: int) -> bool:
  return repository.delete_by_book(db, id_book)