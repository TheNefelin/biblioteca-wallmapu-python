from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import CommuneResponse
from . import repository


async def get_all(db: AsyncSession) -> list[CommuneResponse]:
  items = await repository.get_all(db)
  return [CommuneResponse.model_validate(item) for item in items]
