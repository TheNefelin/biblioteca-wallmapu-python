from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------  
# UPDATE
def update(id_book: int, subject_ids: list[int], db: Session) -> list[dtos.BookSubjectDTO]:
  try:
    (
      db.query(models.BookSubject)
        .filter(models.BookSubject.id_book == id_book)
        .delete(synchronize_session=False)
    )

    relations = []

    for subject_id in subject_ids:
      relation = models.BookSubject(
        id_book=id_book,
        id_subject=subject_id
      )

      db.add(relation)
      relations.append(relation)

    db.commit()
    return [dtos.BookSubjectDTO.model_validate(item) for item in relations]
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
