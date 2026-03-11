from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditionDTO]:
  try:
    query = (
      db.query(models.Edition)
      .order_by(models.Edition.edition.asc())
      .all()
    )

    return [dtos.EditionDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID
def get_by_id(id: int, db: Session) -> dtos.EditionDTO:
  try:
    query = (
      db.query(models.Edition)
      .filter(models.Edition.id_edition == id)
      .first()
    )

    return dtos.EditionDTO.model_validate(query)
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: dtos.CreateEditionDTO, db: Session) -> dtos.EditionDTO:
  try:
    new_item = models.Edition(**data.model_dump())
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return dtos.EditionDTO.model_validate(new_item)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# UPDATE
def update(data: dtos.UpdateEditionDTO, db: Session) -> dtos.EditionDTO:
  try:
    item = (
      db.query(models.Edition)
      .filter(models.Edition.id_edition == data.id_edition)
      .first()
    )

    if not item:
      return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return dtos.EditionDTO.model_validate(item)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# DELETE
def delete(id: int, db: Session) -> bool:
  try:
    item = (
      db.query(models.Edition)
      .filter(models.Edition.id_edition == id)
      .first()
    )
    
    if not item:
      return False

    #if item.images:
    #  raise ValueError("No se puede eliminar la noticia porque tiene imágenes asociadas")

    db.delete(item)
    db.commit()
    return True
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e  
