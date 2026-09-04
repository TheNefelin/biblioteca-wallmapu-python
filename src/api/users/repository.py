from math import ceil
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import UUID

from src.models import models
from src.schemas.dtos import PaginationRequest, PaginationResponse


# -----------------------------------------------------------------
# GET ALL DETAILED
async def get_all_detailed(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse:
  query = (
    select(models.User)
    .options(
      selectinload(models.User.commune),
      selectinload(models.User.user_role),
      selectinload(models.User.user_status),
    )
  )

  if pagination.search:
    query = query.where(
      or_(
        models.User.name.ilike(f"%{pagination.search}%"),
        models.User.lastname.ilike(f"%{pagination.search}%"),
        models.User.email.ilike(f"%{pagination.search}%"),
      )
    )

  items_result = await db.execute(select(func.count()).select_from(query.subquery()))
  items = items_result.scalar_one()
  pages = ceil(items / pagination.limit) if items > 0 else 0

  page = min(pagination.page, pages) if pages > 0 else 1
  skip = (page - 1) * pagination.limit

  result = (await db.execute(
    query.order_by(models.User.updated_at.desc()).offset(skip).limit(pagination.limit)
  )).scalars().all()

  return PaginationResponse(
    page=page,
    pages=pages,
    items=items,
    data=list(result),
  )


# -----------------------------------------------------------------
# GET BY ID DETAILED
async def get_by_id_detailed(
  db: AsyncSession,
  id_user: UUID
) -> models.User | None:
  result = await db.execute(
    select(models.User)
    .options(
      selectinload(models.User.commune),
      selectinload(models.User.user_role),
      selectinload(models.User.user_status),
    )
    .filter(models.User.id_user == id_user)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# GET BY EMAIL
async def get_by_email(db: AsyncSession, email: str) -> models.User | None:
  result = await db.execute(
    select(models.User)
    .options(
      selectinload(models.User.commune),
      selectinload(models.User.user_role),
      selectinload(models.User.user_status),
    )
    .filter(models.User.email == email)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.User:
  user = models.User(**data)
  db.add(user)
  await db.commit()
  await db.refresh(user, ["commune", "user_role", "user_status"])
  return user


# -----------------------------------------------------------------
# GET BY ID USER WITH ROLE AND STATUS
async def get_by_id_with_role_status(db: AsyncSession, id_user: UUID) -> models.User | None:
  result = await db.execute(
    select(models.User)
    .options(
      selectinload(models.User.user_role),
      selectinload(models.User.user_status),
    )
    .filter(models.User.id_user == id_user)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# UPDATE
async def update(
  db: AsyncSession,
  id: UUID,
  update_data: dict
) -> models.User | None:
  entity = await db.get(models.User, id)

  if not entity:
    return None

  for key, value in update_data.items():
    setattr(entity, key, value)

  await db.commit()
  await db.refresh(entity)

  return entity