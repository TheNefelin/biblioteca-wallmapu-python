from math import ceil
from sqlalchemy import or_
from sqlalchemy import UUID
from sqlalchemy.orm import Session, joinedload

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.user_status import models as status_models
from src.api.user_role import models as role_models
from . import models


# -----------------------------------------------------------------
# GET ALL DETAILED
def get_all_detailed(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
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
        models.User.user_role.has(role_models.UserRole.name.ilike(f"%{pagination.search}%")),
        models.User.user_status.has(status_models.UserStatus.name.ilike(f"%{pagination.search}%")),          
      )
    )

  items = query.count()
  pages = ceil(items / pagination.limit) if items > 0 else 0

  page = min(pagination.page, pages) if pages > 0 else 1
  skip = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.User.name.asc())
    .offset(skip)
    .limit(pagination.limit)
    .all()
  )

  return PaginationResponseDTO(
    page=page,
    pages=pages,
    items=items,
    data=result,
  )

# -----------------------------------------------------------------
# GET BY ID DETAILED
def get_by_id_detailed(
  db: Session,
  id_user: UUID
) -> models.User | None:
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
  
# -----------------------------------------------------------------
# GET BY EMAIL
def get_by_email(db: Session, email: str) -> models.User:
  return (
      db.query(models.User)
      .options(
        joinedload(models.User.commune),
        joinedload(models.User.user_role),
        joinedload(models.User.user_status),                
      )
      .filter(models.User.email == email)
      .first()
    )

# -----------------------------------------------------------------
# GET OR CREATE
def get_or_create_user(db: Session, data: dict) -> tuple[models.User, bool]:
  user = (
    db.query(models.User)
    .options(
      joinedload(models.User.user_role),
      joinedload(models.User.user_status),
    )
    .filter(models.User.email == data.get("email"))
    .first()
  )

  if user:
    return user, False

  new_user = models.User(**data)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  user = (
    db.query(models.User)
    .options(
      joinedload(models.User.user_role),
      joinedload(models.User.user_status),
    )
    .filter(models.User.id_user == new_user.id_user)
    .first()
  )
  
  return user, True

# -----------------------------------------------------------------
#UPDATE
def update(
  db: Session,
  id: UUID, 
  update_data: dict
) -> models.User | None:
  entity = db.query(models.User).filter(models.User.id_user == id).first()
  
  if not entity:
    return None
  
  for key, value in update_data.items():
    setattr(entity, key, value)
  
  db.commit()
  db.refresh(entity)

  return entity  
