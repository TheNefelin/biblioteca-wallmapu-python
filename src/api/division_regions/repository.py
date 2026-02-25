from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.RegionDTO]:
  try:
    query = (
      db.query(models.Region)
      .order_by(models.Region.region.asc())
      .all()
    )
    
    return [dtos.RegionDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
  