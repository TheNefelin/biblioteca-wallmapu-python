from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.AuthorDTO]:
  try:
    query = (
      db.query(models.Author)
      .order_by(models.Author.name.asc())
      .all()  
    )

    return [dtos.AuthorDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e

