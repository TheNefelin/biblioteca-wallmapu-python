from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, dtos

def get_all(db: Session):
  try:
    return db.query(models.User).all()
  except SQLAlchemyError as e:
    raise e
  
def get_by_id(db: Session, id_user: int):
  try:
    return db.query(models.User).filter(models.User.id_user == id_user).first()
  except SQLAlchemyError as e:
    raise e
  
def create(db: Session, user_data: dtos.CreateUserDTO):
  try:
    # Convertir DTO a dict y crear modelo
    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Obtener id_user, created_at, etc.
    return new_user
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
  
def update(db: Session, id_user: int, user_data: dtos.UpdateUserDTO):
  try:
    # Buscar usuario existente
    user = db.query(models.User).filter(models.User.id_user == id_user).first()
    if not user:
      return None
    
    # Solo actualizar campos que vienen en el request (exclude_unset=True)
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user
  except IntegrityError as e:
    db.rollback()
    if 'rut' in str(e.orig):
      raise ValueError("El RUT ya está registrado por otro usuario")
    else:
      raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e  