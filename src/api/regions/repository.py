from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.regions.models import Region
from . import dtos

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.RegionDTO]:
  try:
    items = (
      db.query(Region)
      .order_by(Region.id_region.asc())
      .all()
    )
    
    return [dtos.RegionDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  