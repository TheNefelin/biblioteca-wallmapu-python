from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import models


# -----------------------------------------------------------------
# GET ALL DETAIL (una sola query, solo columnas del DTO)
def _build_detail_query():
  return (
    select(
      models.Copy.id_copy,
      models.Copy.barcode,
      models.Copy.signature_topography,
      models.Copy.copy_number,
      models.Copy.created_at,
      models.Copy.updated_at,
      models.Copy.status_id,
      models.CopyStatus.name.label("status_name"),
      models.Copy.edition_id,
      models.Edition.edition.label("edition_name"),
      models.Edition.isbn.label("edition_isbn"),
      models.Edition.cover_image.label("edition_cover_image"),
      func.coalesce(models.Editorial.id_editorial, 0).label("editorial_id"),
      func.coalesce(models.Editorial.name, "Sin Editorial").label("editorial_name"),
    )
    .join(models.CopyStatus, models.Copy.status_id == models.CopyStatus.id_status)
    .join(models.Edition, models.Copy.edition_id == models.Edition.id_edition)
    .outerjoin(models.Editorial, models.Edition.editorial_id == models.Editorial.id_editorial)
  )


async def get_all_detail_by_edition_id(db: AsyncSession, edition_id: int) -> list:
  result = await db.execute(
    _build_detail_query()
    .where(models.Copy.edition_id == edition_id)
    .order_by(models.Copy.id_copy.asc())
  )
  return result.all()


async def get_all_detail_by_book_id(db: AsyncSession, book_id: int) -> list:
  result = await db.execute(
    _build_detail_query()
    .where(models.Edition.book_id == book_id)
    .order_by(models.Copy.id_copy.asc())
  )
  return result.all()


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> models.Copy | None:
  result = await db.execute(
    select(models.Copy)
    .options(selectinload(models.Copy.status))
    .where(models.Copy.id_copy == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CHECK IF SIGNATURE EXISTS
async def signature_exists(db: AsyncSession, signature: str, exclude_id: int = 0) -> bool:
  stmt = select(models.Copy.signature_topography).where(
    models.Copy.signature_topography == signature
  )
  if exclude_id > 0:
    stmt = stmt.where(models.Copy.id_copy != exclude_id)
  result = await db.execute(stmt)
  return result.first() is not None


# -----------------------------------------------------------------
# CHECK IF COPY NUMBER EXISTS FOR EDITION
async def copy_number_exists(db: AsyncSession, edition_id: int, copy_number: int, exclude_id: int = 0) -> bool:
  stmt = select(models.Copy.copy_number).where(
    models.Copy.edition_id == edition_id,
    models.Copy.copy_number == copy_number
  )
  if exclude_id > 0:
    stmt = stmt.where(models.Copy.id_copy != exclude_id)
  result = await db.execute(stmt)
  return result.first() is not None


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Copy:
  item = models.Copy(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, item: models.Copy, data: dict) -> models.Copy:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, item: models.Copy) -> None:
  await db.delete(item)
  await db.commit()


# -----------------------------------------------------------------
# UPDATE STATUS (usado por loans service)
async def update_status(db: AsyncSession, copy_id: int, status_id: int) -> bool:
  item = (await db.execute(
    select(models.Copy).where(models.Copy.id_copy == copy_id)
  )).scalar_one_or_none()
  if not item:
    return False
  item.status_id = status_id
  await db.commit()
  return True


# -----------------------------------------------------------------
# UPDATE ALL OVERDUE STATUS (usado por loans service para actualizar copies de loans vencidos)
async def update_all_overdue_status(db: AsyncSession) -> int:
  loaned_subq = (
    select(models.Loan.copy_id)
    .where(models.Loan.loan_status_id == 3)
  )
  result = await db.execute(
    models.Copy.__table__.update()
    .where(
      models.Copy.status_id == 1,
      models.Copy.id_copy.in_(loaned_subq)
    )
    .values(status_id=2)
  )
  await db.commit()
  return result.rowcount