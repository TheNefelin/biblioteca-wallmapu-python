from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models


# -----------------------------------------------------------------
# UPDATE
def update(id_book: int, author_ids: list[int], db: Session) -> list[dtos.BookAuthorDTO]:
  try:
    # evitar duplicados
    author_ids = list(set(author_ids))

    # eliminar relaciones actuales
    db.query(models.BookAuthor).filter(
      models.BookAuthor.id_book == id_book
    ).delete(synchronize_session=False)

    # crear nuevas relaciones solo si hay IDs
    relations = [
      models.BookAuthor(id_book=id_book, id_author=aid)
      for aid in author_ids
    ]

    if relations:
      db.add_all(relations)

    db.commit()

    return [dtos.BookAuthorDTO.model_validate(r) for r in relations]
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------  
# DELETE
def delete(item: dtos.BookAuthorDTO, db: Session) -> bool:
  try:
    relation = db.get(
      models.BookAuthor,
      (item.id_book, item.id_author)
    )

    if not relation:
      return False

    db.delete(relation)
    db.commit()

    return True
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e  