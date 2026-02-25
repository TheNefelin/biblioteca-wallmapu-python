from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditorialDTO]:
  try:
    query = (
      db.query(models.Editorial)
      .order_by(models.Editorial.editorial.asc())
      .all()
    )

    return [dtos.EditorialDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
