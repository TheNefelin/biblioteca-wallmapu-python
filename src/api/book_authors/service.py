from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si author_ids viene vacío, elimina todas)
def update_authors(id_book: int, author_ids: list[int], db: Session) -> list[dtos.BookAuthorDTO]:
  items = repository.update(id_book, author_ids or [], db)
  return [dtos.BookAuthorDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación book-author)
def delete_author(id_book: int, id_author: int, db: Session) -> bool:
  item = dtos.BookAuthorDTO(id_book=id_book, id_author=id_author)
  res = repository.delete(item, db)
  return res
