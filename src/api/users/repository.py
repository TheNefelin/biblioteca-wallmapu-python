from sqlite3 import IntegrityError
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models, dtos

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session):
  try:
    entities = db.query(models.User).all()
    dtos =  [dtos.UserDTO.model_validate(entity) for entity in entities]

    return dtos
  except SQLAlchemyError as e:
    raise e

# GET BY ID
def get_by_id(id_user: UUID, db: Session):
  try:
    entity = db.query(models.User).filter(models.User.id_user == id_user).first()
    dto = dtos.UserDTO.model_validate(entity)
    
    return dto
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(create_dto: dtos.CreateUserDTO, db: Session):
  try:
    entity = models.User(**create_dto.model_dump())
    
    db.add(entity)
    db.commit()
    db.refresh(entity)
    
    dto = dtos.UserDTO.model_validate(entity)
    return dto
  except IntegrityError as e:
    db.rollback()
    # Detectar si es error de email o rut duplicado
    if 'email' in str(e.orig):
      raise ValueError("El email ya está registrado")
    elif 'rut' in str(e.orig):
      raise ValueError("El RUT ya está registrado")
    else:
      raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
#UPDATE
def update(id_user: UUID, update_dto: dtos.UpdateUserDTO, db: Session):
  try:
    entity = db.query(models.User).filter(models.User.id_user == id_user).first()
    
    if not entity:
      return None
    
    # Solo actualizar campos que vienen en el request (exclude_unset=True)
    update_data = update_dto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(entity, key, value)
    
    db.commit()
    db.refresh(entity)

    dto = dtos.UserDTO.model_validate(entity)
    return dto
  except IntegrityError as e:
    db.rollback()
    if 'rut' in str(e.orig):
      raise ValueError("El RUT ya está registrado por otro usuario")
    else:
      raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e  