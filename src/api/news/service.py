from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


def get_all_pagination(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO[list[dtos.NewsWithGalleryDTO]]:
  page = repository.get_all_pagination(pagination, db)
  return PaginationResponseDTO[list[dtos.NewsWithGalleryDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[dtos.NewsWithGalleryDTO.model_validate(item) for item in page.data],
    next=page.next,
    prev=page.prev,
  )


def get_by_id(id: int, db: Session) -> dtos.NewsWithGalleryDTO | None:
  entity = repository.get_by_id(id, db)
  if not entity:
    return None
  return dtos.NewsWithGalleryDTO.model_validate(entity)


def create(data: dtos.CreateNewsDTO, db: Session) -> dtos.NewsDTO:
  entity = repository.create(data.model_dump(), db)
  return dtos.NewsDTO.model_validate(entity)


def update(id: int, data: dtos.UpdateNewsDTO, db: Session) -> dtos.NewsDTO | None:
  entity = repository.update(id, data.model_dump(exclude_unset=True), db)
  if not entity:
    return None
  return dtos.NewsDTO.model_validate(entity)


def delete(id: int, db: Session) -> bool:
  return repository.delete(id, db)

