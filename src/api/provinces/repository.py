from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, dtos

# GET ALL
def get_all(db: Session):
  try:
    items = db.query(models.Province).all()
    
    return [dtos.ProvinceDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  