from sqlalchemy.orm import Session

from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.AuthorDTO]:
  authors = repository.get_all(db)
  return [dtos.AuthorDTO.model_validate(a) for a in authors]
