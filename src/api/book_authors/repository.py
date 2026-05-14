from sqlalchemy.orm import Session

from . import models


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id_book: int, author_ids: list[int]) -> list[models.BookAuthor]:
  db.query(models.BookAuthor).filter(
    models.BookAuthor.id_book == id_book
  ).delete(synchronize_session=False)

  relations = [
    models.BookAuthor(id_book=id_book, id_author=aid)
    for aid in author_ids
  ]

  if relations:
    db.add_all(relations)

  db.commit()

  return relations


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id_book: int, id_author: int) -> bool:
  relation = db.get(
    models.BookAuthor,
    (id_book, id_author)
  )

  if not relation:
    return False

  db.delete(relation)
  db.commit()

  return True


# -----------------------------------------------------------------
# GET BY BOOK
def get_by_book(db: Session, id_book: int) -> list[models.BookAuthor]:
  return (
    db.query(models.BookAuthor)
    .filter(models.BookAuthor.id_book == id_book)
    .all()
  )


# -----------------------------------------------------------------
# DELETE BY ID BOOK
def delete_by_book(db: Session, id_book: int) -> bool:
  rows_deleted = (
    db.query(models.BookAuthor)
    .filter(models.BookAuthor.id_book == id_book)
    .delete(synchronize_session=False)
  )

  db.commit()

  return rows_deleted > 0