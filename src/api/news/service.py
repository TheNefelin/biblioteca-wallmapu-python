from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.schemas.dtos import PaginationRequest, PaginationResponse
from src.schemas.dtos import NewsRequest, NewsResponse, NewsWithGalleryResponse, NewsRequest
from . import repository


async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse[list[NewsWithGalleryResponse]]:
  page = await repository.get_all_pagination(db, pagination)
  return PaginationResponse[list[NewsWithGalleryResponse]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[NewsWithGalleryResponse.model_validate(item) for item in page.data],
    next=page.next,
    prev=page.prev,
  )


async def get_by_id(db: AsyncSession, id: int) -> NewsWithGalleryResponse | None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    return None
  return NewsWithGalleryResponse.model_validate(entity)


async def create(db: AsyncSession, data: NewsRequest) -> NewsResponse:
  entity = await repository.create(db, data.model_dump(exclude_unset=True))
  return NewsResponse.model_validate(entity)


async def update(db: AsyncSession, id: int, data: NewsRequest) -> NewsResponse | None:
  entity = await repository.update(db, id, data.model_dump(exclude_unset=True))
  if not entity:
    return None
  return NewsResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> bool:
  entity = await repository.get_by_id(db, id)
  if not entity:
    return False

  if entity.images:
    raise BadRequestProblem(detail="No se puede eliminar la noticia porque tiene imágenes asociadas")

  return await repository.delete(db, id)