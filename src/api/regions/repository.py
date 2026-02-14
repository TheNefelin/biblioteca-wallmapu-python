from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.regions.dtos import RegionDTO
from src.api.regions.models import Region

# GET ALL
def get_all(db: Session):
  try:
    items = db.query(Region).order_by(Region.id_region.asc()).all()
    
    return [RegionDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  