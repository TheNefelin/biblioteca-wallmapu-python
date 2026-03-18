from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.CopyStatusDTO]:
  try:
    query = (
      db.query(models.CopyStatus)
      .order_by(models.CopyStatus.name.asc())
      .all()
    )
    
    return [dtos.CopyStatusDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e