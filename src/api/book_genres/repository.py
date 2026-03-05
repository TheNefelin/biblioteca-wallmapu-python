from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.GenreDTO]:
  try:
    query = (
      db.query(models.Genre)
      .order_by(models.Genre.name.asc())
      .all()
    )

    return [dtos.GenreDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
