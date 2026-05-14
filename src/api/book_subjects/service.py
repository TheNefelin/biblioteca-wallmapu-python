from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, elimina todas)
def update_subjects(db: Session, id_book: int, subject_ids: list[int]) -> list[dtos.BookSubjectDTO]:
  subject_ids = list(set(subject_ids or []))
  items = repository.update(db, id_book, subject_ids)
  return [dtos.BookSubjectDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación book-subject)
def delete_subject(db: Session, id_book: int, id_subject: int) -> bool:
  return repository.delete(db, id_book, id_subject)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciónes book-subject)
def delete_subject_by_book(db: Session, id_book: int) -> bool:
  return repository.delete_by_book(db, id_book)