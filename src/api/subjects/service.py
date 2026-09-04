from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError, DuplicateNameError, NotFoundError
from src.schemas.dtos import SubjectResponse
from src.schemas.dtos import PaginationRequest, PaginationResponse
from . import repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse:
  pagination_response = await repository.get_all_pagination(db, pagination)
  items = pagination_response.data or []

  data = [SubjectResponse.model_validate(item) for item in items]

  return PaginationResponse(
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[SubjectResponse]:
  items = await repository.get_all(db)
  return [SubjectResponse.model_validate(item) for item in items]


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, dto) -> SubjectResponse:
  if await repository.get_by_name(db, dto.name):
    raise DuplicateNameError(dto.name)

  created = await repository.create(db, dto.model_dump(exclude_unset=True))

  if not created or not created.id_subject:
    raise NotFoundError("Descriptor")

  return SubjectResponse.model_validate(created)


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id: int, dto) -> SubjectResponse:
  existing = await repository.get_by_name(db, dto.name)
  if existing and existing.id_subject != id:
    raise DuplicateNameError(dto.name)

  updated = await repository.update(db, id, dto.model_dump(exclude_unset=True))

  if not updated:
    raise NotFoundError("Descriptor")

  return SubjectResponse.model_validate(updated)


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id: int) -> bool:
  result = await repository.delete(db, id)

  if result is None:
    raise NotFoundError("Descriptor")

  if result is False:
    raise AppError("No se puede eliminar: el descriptor tiene libros asociados")

  return result
