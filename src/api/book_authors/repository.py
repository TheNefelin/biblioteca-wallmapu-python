from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import models


# -----------------------------------------------------------------
# UPDATE
def update(id_book: int, author_ids: list[int], db: Session) -> list[models.BookAuthor]:
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

    return relations
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------  
# DELETE
def delete(id_book: int, id_author: int, db: Session) -> bool:
  try:
    relation = db.get(
      models.BookAuthor,
      (id_book, id_author)
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