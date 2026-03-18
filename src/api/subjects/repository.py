from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Subject]:
  try:
    return (
      db.query(models.Subject)
      .order_by(models.Subject.name.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
