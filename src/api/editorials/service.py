from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError, DuplicateNameError, NotFoundError
from src.schemas.dtos import EditorialResponse
from src.schemas.dtos import PaginationRequest, PaginationResponse
from . import repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse:
  pagination_response = await repository.get_all_pagination(db, pagination)
  items = pagination_response.data or []

  data = [EditorialResponse.model_validate(item) for item in items]

  return PaginationResponse(
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[EditorialResponse]:
  items = await repository.get_all(db)
  return [EditorialResponse.model_validate(item) for item in items]


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> EditorialResponse | None:
  item = await repository.get_by_id(db, id)
  if not item:
    return None
  return EditorialResponse.model_validate(item)


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, dto) -> EditorialResponse:
  if await repository.exists_by_name(db, dto.name):
    raise DuplicateNameError(dto.name)

  data = dto.model_dump()

  entity = await repository.create(db, data)
  return EditorialResponse.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id: int, dto) -> EditorialResponse:
  if not await repository.exists_by_id(db, id):
    raise NotFoundError("Editorial")

  if await repository.exists_by_name(db, dto.name, exclude_id=id):
    raise DuplicateNameError(dto.name)

  current = await repository.get_by_id(db, id)
  update_data = dto.model_dump(exclude={"id_editorial"})

  entity = await repository.update(db, current, update_data)
  return EditorialResponse.model_validate(entity)


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id: int) -> bool:
  result = await repository.delete(db, id)

  if result is None:
    raise NotFoundError("Editorial")

  if result is False:
    raise AppError("No se puede eliminar: la editorial tiene ediciones asociadas")

  return result
