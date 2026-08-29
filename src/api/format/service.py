from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError, DuplicateNameError, NotFoundError
from src.schemas.dtos import FormatResponse
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import repository


# -----------------------------------------------------------------#
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  pagination_response = await repository.get_all_pagination(db, pagination)
  items = pagination_response.data or []

  data = [FormatResponse.model_validate(item) for item in items]

  return PaginationResponseDTO(
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------#
# GET ALL
async def get_all(db: AsyncSession) -> list[FormatResponse]:
  items = await repository.get_all(db)
  return [FormatResponse.model_validate(item) for item in items]


# -----------------------------------------------------------------#
# CREATE
async def create(db: AsyncSession, dto) -> FormatResponse:
  if await repository.get_by_name(db, dto.name):
    raise DuplicateNameError(dto.name)

  created = await repository.create(db, dto.model_dump(exclude_unset=True))

  if not created or not created.id_format:
    raise NotFoundError("Formato")

  return FormatResponse.model_validate(created)


# -----------------------------------------------------------------#
# UPDATE
async def update(db: AsyncSession, id: int, dto) -> FormatResponse:
  existing = await repository.get_by_name(db, dto.name)
  if existing and existing.id_format != id:
    raise DuplicateNameError(dto.name)

  updated = await repository.update(db, id, dto.model_dump(exclude_unset=True))

  if not updated:
    raise NotFoundError("Formato")

  return FormatResponse.model_validate(updated)


# -----------------------------------------------------------------#
# DELETE
async def delete(db: AsyncSession, id: int) -> bool:
  result = await repository.delete(db, id)

  if result is None:
    raise NotFoundError("Formato")

  if result is False:
    raise AppError("No se puede eliminar: el formato tiene ediciones asociadas")

  return result
