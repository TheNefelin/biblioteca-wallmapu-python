from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, elimina todas)
def update_subjects(id_book: int, subject_ids: list[int], db: Session) -> list[dtos.BookSubjectDTO]:
  items = repository.update(id_book, subject_ids or [], db)
  return [dtos.BookSubjectDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación book-subject)
def delete_subject(id_book: int, id_subject: int, db: Session) -> bool:
  item = dtos.BookSubjectDTO(id_book=id_book, id_subject=id_subject)
  return repository.delete(item, db)
