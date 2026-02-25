from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.CommuneDTO]:
  try:
    query = (
      db.query(models.Commune)
      .order_by(models.Commune.commune.asc())
      .all()
    )
    
    return [dtos.CommuneDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
  