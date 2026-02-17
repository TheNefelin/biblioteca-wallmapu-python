from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# GET ALL
def get_all(db: Session):
  try:
    items = db.query(models.Commune).all()
    
    return [dtos.CommuneDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  