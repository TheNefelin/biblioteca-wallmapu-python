from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import UserRoleDTO
from . import repository


async def get_all(db: AsyncSession) -> list[UserRoleDTO]:
  items = await repository.get_all(db)
  return [UserRoleDTO.model_validate(item) for item in items]
