from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, dtos

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.ProvinceDTO]:
  try:
    query = (
      db.query(models.Province)
      .order_by(models.Province.province.asc())
      .all()
    )
    
    return [dtos.ProvinceDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
  