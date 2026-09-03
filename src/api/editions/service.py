from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import EditionDTO, EditionDetailDTO, EditionFilterDTO, SaveEditionDTO
from src.core import cloudinary
from src.api.edition_format import service as edition_format_service
from . import repository


# -----------------------------------------------------------------
# GET ALL PAGINATION REAL (flat DTO)
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO[EditionFilterDTO]) -> PaginationResponseDTO[list[EditionDetailDTO]]:
  response = await repository.get_all_pagination(db, pagination)
  editions = response.data or []
  data = [EditionDetailDTO.model_validate(dict(item._mapping)) for item in editions]

  return PaginationResponseDTO[list[EditionDetailDTO]](
    page=response.page,
    pages=response.pages,
    items=response.items,
    data=data,
    next=response.next,
    prev=response.prev,
  )


# -----------------------------------------------------------------
# GET BY BOOK ID DETAIL (flat DTO)
async def get_all_by_book_id_detail(db: AsyncSession, book_id: int) -> list[EditionDetailDTO]:
  rows = await repository.get_by_book_id_detail(db, book_id)
  return [EditionDetailDTO.model_validate(dict(row._mapping)) for row in (rows or [])]


# -----------------------------------------------------------------
# GET BY BOOK ID (básico)
async def get_by_book_id(db: AsyncSession, book_id: int) -> list[EditionDTO]:
  editions = await repository.get_by_book_id(db, book_id)
  return [EditionDTO.model_validate(e) for e in editions]


# -----------------------------------------------------------------
# GET BY ID (básico)
async def get_edition_by_id(db: AsyncSession, id: int) -> EditionDTO | None:
  edition = await repository.get_by_id(db, id)
  if not edition:
    return None
  return EditionDTO.model_validate(edition)


# -----------------------------------------------------------------
# CREATE
async def create_edition(db: AsyncSession, data: SaveEditionDTO) -> EditionDTO:
  dump = data.model_dump()
  format_ids = dump.pop("format_ids", None)

  created = await repository.create(db, dump)

  if format_ids is not None:
    await edition_format_service.update_formats(db, created.id_edition, format_ids)

  return EditionDTO.model_validate(await repository.get_by_id(db, created.id_edition))


# -----------------------------------------------------------------
# UPDATE
async def update_edition(db: AsyncSession, id: int, data: SaveEditionDTO) -> EditionDTO | None:
  edition = await repository.get_entity_by_id(db, id)
  if not edition:
    return None

  dump = data.model_dump(exclude_unset=True)
  format_ids = dump.pop("format_ids", None)

  updated = await repository.update(db, edition, dump)

  if format_ids is not None:
    await edition_format_service.update_formats(db, updated.id_edition, format_ids)

  return EditionDTO.model_validate(await repository.get_by_id(db, updated.id_edition))


# -----------------------------------------------------------------
# DELETE
async def delete_edition_with_image(db: AsyncSession, id: int) -> bool:
  edition = await repository.get_entity_by_id(db, id)
  if not edition:
    return False

  if await repository.has_copies(db, edition.id_edition):
    raise BadRequestProblem(detail=f"La edición ({edition.edition}) tiene copias asociadas")

  url = await repository.delete(db, edition)

  if url:
    public_id = cloudinary.extract_public_id(url)
    cloudinary.delete_image(public_id)

  return True