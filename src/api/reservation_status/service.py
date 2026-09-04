from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import ReservationStatusResponse
from . import repository


async def get_all(db: AsyncSession) -> list[ReservationStatusResponse]:
  items = await repository.get_all(db)
  return [ReservationStatusResponse.model_validate(item) for item in items]
