from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, solo elimina)
def update(id_book: int, subject_ids: list[int], db: Session) -> list[models.BookSubject]:
  try:
    # evitar duplicados
    subject_ids = list(set(subject_ids))

    # eliminar relaciones actuales
    db.query(models.BookSubject).filter(
      models.BookSubject.id_book == id_book
    ).delete(synchronize_session=False)

    # crear nuevas relaciones solo si hay IDs
    relations = [
      models.BookSubject(id_book=id_book, id_subject=sid)
      for sid in subject_ids
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
def delete(item: dtos.BookSubjectDTO, db: Session) -> bool:
  try:
    relation = db.get(
      models.BookSubject,
      (item.id_book, item.id_subject)
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
