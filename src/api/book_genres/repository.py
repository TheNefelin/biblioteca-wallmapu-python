from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.BookGenreDTO]:
  try:
    query = (
      db.query(models.BookGenre)
      .order_by(models.BookGenre.name.asc())
      .all()
    )

    return [dtos.BookGenreDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
