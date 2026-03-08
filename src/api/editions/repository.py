from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditionDTO]:
  try:
    query = (
      db.query(models.Edition)
      .order_by(models.Edition.edition.asc())
      .all()
    )

    return [dtos.EditionDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
