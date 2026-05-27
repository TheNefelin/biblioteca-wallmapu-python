from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si format_ids viene vacío, elimina todas)
def update_formats(db: Session, id_edition: int, format_ids: list[int]) -> list[dtos.EditionFormatDTO]:
  format_ids = list(set(format_ids or []))
  items = repository.update(db, id_edition, format_ids)
  return [dtos.EditionFormatDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relación edition-format)
def delete_format(db: Session, id_edition: int, id_format: int) -> bool:
  return repository.delete(db, id_edition, id_format)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciones edition-format)
def delete_format_by_edition(db: Session, id_edition: int) -> bool:
  return repository.delete_by_edition(db, id_edition)
