from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import EditionFormatResponse
from . import repository


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si format_ids viene vacÃ­o, elimina todas)
async def update_formats(db: AsyncSession, id_edition: int, format_ids: list[int]) -> list[EditionFormatResponse]:
  format_ids = list(set(format_ids or []))
  items = await repository.update(db, id_edition, format_ids)
  return [EditionFormatResponse.model_validate(item) for item in items]


# -----------------------------------------------------------------
# DELETE (elimina una relaciÃ³n edition-format)
async def delete_format(db: AsyncSession, id_edition: int, id_format: int) -> bool:
  return await repository.delete(db, id_edition, id_format)


# -----------------------------------------------------------------
# DELETE (elimina toda las relaciones edition-format)
async def delete_format_by_edition(db: AsyncSession, id_edition: int) -> bool:
  return await repository.delete_by_edition(db, id_edition)