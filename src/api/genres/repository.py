from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Genre]:
  try:
    return (
      db.query(models.Genre)
      .order_by(models.Genre.name.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
