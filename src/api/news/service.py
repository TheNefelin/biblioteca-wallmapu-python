from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.NewsWithGalleryDTO]]:
  page = repository.get_all_pagination(db, pagination)
  return PaginationResponseDTO[list[dtos.NewsWithGalleryDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[dtos.NewsWithGalleryDTO.model_validate(item) for item in page.data],
    next=page.next,
    prev=page.prev,
  )


def get_by_id(db: Session, id: int) -> dtos.NewsWithGalleryDTO | None:
  entity = repository.get_by_id(db, id)
  if not entity:
    return None
  return dtos.NewsWithGalleryDTO.model_validate(entity)


def create(db: Session, data: dtos.CreateNewsDTO) -> dtos.NewsDTO:
  entity = repository.create(db, data.model_dump())
  return dtos.NewsDTO.model_validate(entity)


def update(db: Session, id: int, data: dtos.UpdateNewsDTO) -> dtos.NewsDTO | None:
  entity = repository.update(db, id, data.model_dump(exclude_unset=True))
  if not entity:
    return None
  return dtos.NewsDTO.model_validate(entity)


def delete(db: Session, id: int) -> bool:
  entity = repository.get_by_id(db, id)
  if not entity:
    return False
  
  if entity.images:
    raise ValueError("No se puede eliminar la noticia porque tiene imágenes asociadas")
  
  return repository.delete(db, id)