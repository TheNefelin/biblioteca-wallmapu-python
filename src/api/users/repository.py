from math import ceil
from sqlalchemy import or_
from sqlite3 import IntegrityError
from sqlalchemy import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from src.api.user_status import models as status_models
from src.api.user_role import models as role_models
from . import models, dtos

# -----------------------------------------------------------------
# GET ALL DETAILED
def get_all_detailed(
  page: int, 
  items: int, 
  search: str | None, 
  db: Session
) -> tuple[int, int, list[dtos.UserDetailDTO]]:
  try:
    query = (
      db.query(models.User)
      .options(
        joinedload(models.User.commune),
        joinedload(models.User.user_role),
        joinedload(models.User.user_status),                
      )
    )

    if search:
      search_filter = or_(
        models.User.name.ilike(f"%{search}%"),
        models.User.lastname.ilike(f"%{search}%"),
        models.User.email.ilike(f"%{search}%"),
        models.User.user_role.has(role_models.UserRole.role.ilike(f"%{search}%")),
        models.User.user_status.has(status_models.UserStatus.status.ilike(f"%{search}%")),
      )
      query = query.filter(search_filter)    

    # Paginación
    count = query.order_by(None).count()
    pages = ceil(count / items) if count > 0 else 0
    offset = (page - 1) * items

    result = (
      query
      .order_by(models.User.created_at.desc())
      .offset(offset)
      .limit(items)
      .all()
    )

    dto_list = [dtos.UserDetailDTO.model_validate(item)for item in result]
    return count, pages, dto_list
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID DETAILED
def get_by_id_detailed(
  id_user: UUID, 
  db: Session
) -> dtos.UserDetailDTO | None:
  try:
    entity = (
      db.query(models.User)
      .options(
        joinedload(models.User.commune),
        joinedload(models.User.user_role),
        joinedload(models.User.user_status),                
      )
      .filter(models.User.id_user == id_user)
      .first()
    )

    if not entity:
      return None

    dto = dtos.UserDetailDTO.model_validate(entity)
    return dto
  except SQLAlchemyError as e:
    raise e
  
# -----------------------------------------------------------------
# GET OR CREATE
def get_or_create_user(
  email: str,
  name: str,
  db: Session
) -> dtos.UserWithRoleDTO:
  try:
    user = (
      db.query(models.User)
      .options(joinedload(models.User.user_role))
      .filter(models.User.email == email)
      .first()
    )

    if user:
      return dtos.UserWithRoleDTO.model_validate(user)

    new_user = models.User(
      email=email,
      name=name,
      user_role_id=3,
      user_status_id=1
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user = (
        db.query(models.User)
        .options(joinedload(models.User.user_role))
        .filter(models.User.id_user == new_user.id_user)
        .first()
    )
    
    return dtos.UserWithRoleDTO.model_validate(user)
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
#UPDATE
def update(
  id: UUID, 
  update_dto: dtos.UpdateUserDTO, 
  db: Session
) -> dtos.UserDTO | None:
  try:
    entity = db.query(models.User).filter(models.User.id_user == id).first()
    
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