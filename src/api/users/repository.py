from math import ceil
from sqlalchemy import or_
from sqlalchemy import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.user_status import models as status_models
from src.api.user_role import models as role_models
from . import models


# -----------------------------------------------------------------
# GET ALL DETAILED
def get_all_detailed(
  pagination: PaginationRequestDTO, 
  db: Session
) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.User)
      .options(
        joinedload(models.User.commune),
        joinedload(models.User.user_role),
        joinedload(models.User.user_status),                
      )
    )

    if pagination.search:
      query = query.filter(
        or_(
          models.User.name.ilike(f"%{pagination.search}%"),
          models.User.lastname.ilike(f"%{pagination.search}%"),
          models.User.email.ilike(f"%{pagination.search}%"),
          models.User.user_role.has(role_models.UserRole.role.ilike(f"%{pagination.search}%")),
          models.User.user_status.has(status_models.UserStatus.name.ilike(f"%{pagination.search}%")),          
        )
      )

    items = query.count()
    pages = ceil(items / pagination.limit) if items > 0 else 0

    # Ajuste seguro de página
    page = min(pagination.page, pages) if pages > 0 else 1
    skip = (page - 1) * pagination.limit

    result = (
      query
      .order_by(models.User.name.asc())
      .offset(skip)
      .limit(pagination.limit)
      .all()
    )

    next_url = f"/api/users/pagination?page={page + 1}&limit={pagination.limit}" if page < pages else None
    prev_url = f"/api/users/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

    return PaginationResponseDTO(
      page=page,
      pages=pages,
      items=items,
      data=result,
      next=next_url,
      prev=prev_url
    )
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID DETAILED
def get_by_id_detailed(
  id_user: UUID, 
  db: Session
) -> models.User | None:
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

    return entity
  except SQLAlchemyError as e:
    raise e
  
# -----------------------------------------------------------------
# GET OR CREATE
def get_or_create_user(
  email: str,
  name: str,
  db: Session
) -> models.User:
  try:
    user = (
      db.query(models.User)
      .options(joinedload(models.User.user_role))
      .filter(models.User.email == email)
      .first()
    )

    if user:
      return user

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
    
    return user
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
  update_data: dict, 
  db: Session
) -> models.User | None:
  try:
    entity = db.query(models.User).filter(models.User.id_user == id).first()
    
    if not entity:
      return None
    
    # Solo actualizar campos que vienen en el request (exclude_unset=True)
    for key, value in update_data.items():
      setattr(entity, key, value)
    
    db.commit()
    db.refresh(entity)

    return entity
  except IntegrityError as e:
    db.rollback()
    if 'rut' in str(e.orig):
      raise ValueError("El RUT ya está registrado por otro usuario")
    else:
      raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e  