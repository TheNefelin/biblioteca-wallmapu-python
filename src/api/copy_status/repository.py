from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.CopyStatus]:
  try:
    return (
      db.query(models.CopyStatus)
      .order_by(models.CopyStatus.name.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, status_id: int) -> models.CopyStatus | None:
  try:
    return db.query(models.CopyStatus).filter(models.CopyStatus.id_status == status_id).first()
  except SQLAlchemyError as e:
    raise e