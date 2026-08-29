from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import CreateNewsDTO, NewsDTO, NewsWithGalleryDTO, UpdateNewsDTO
from . import repository


async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[NewsWithGalleryDTO]]:
  page = await repository.get_all_pagination(db, pagination)
  return PaginationResponseDTO[list[NewsWithGalleryDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[NewsWithGalleryDTO.model_validate(item) for item in page.data],
    next=page.next,
    prev=page.prev,
  )


async def get_by_id(db: AsyncSession, id: int) -> NewsWithGalleryDTO | None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    return None
  return NewsWithGalleryDTO.model_validate(entity)


async def create(db: AsyncSession, data: CreateNewsDTO) -> NewsDTO:
  entity = await repository.create(db, data.model_dump())
  return NewsDTO.model_validate(entity)


async def update(db: AsyncSession, id: int, data: UpdateNewsDTO) -> NewsDTO | None:
  entity = await repository.update(db, id, data.model_dump(exclude_unset=True))
  if not entity:
    return None
  return NewsDTO.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> bool:
  entity = await repository.get_by_id(db, id)
  if not entity:
    return False

  if entity.images:
    raise ValueError("No se puede eliminar la noticia porque tiene imágenes asociadas")

  return await repository.delete(db, id)