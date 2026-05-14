from sqlalchemy.orm import Session

from . import models


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, solo elimina)
def update(db: Session, id_book: int, subject_ids: list[int]) -> list[models.BookSubject]:
  db.query(models.BookSubject).filter(
    models.BookSubject.id_book == id_book
  ).delete(synchronize_session=False)

  relations = [
    models.BookSubject(id_book=id_book, id_subject=sid)
    for sid in subject_ids
  ]

  if relations:
    db.add_all(relations)

  db.commit()

  return relations


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id_book: int, id_subject: int) -> bool:
  relation = db.get(
    models.BookSubject,
    (id_book, id_subject)
  )

  if not relation:
    return False

  db.delete(relation)
  db.commit()

  return True


# -----------------------------------------------------------------
# GET BY BOOK
def get_by_book(db: Session, id_book: int) -> list[models.BookSubject]:
  return (
    db.query(models.BookSubject)
    .filter(models.BookSubject.id_book == id_book)
    .all()
  )


# -----------------------------------------------------------------
# DELETE BY ID BOOK
def delete_by_book(db: Session, id_book: int) -> bool:
  rows_deleted = (
    db.query(models.BookSubject)
    .filter(models.BookSubject.id_book == id_book)
    .delete(synchronize_session=False)
  )

  db.commit()

  return rows_deleted > 0