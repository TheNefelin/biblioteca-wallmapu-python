from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.schemas.dtos import LoanStatusResponse
from . import service

router = APIRouter(
  prefix="/loan-status",
  tags=["loan-status"],
)

@router.get(
  "/",
  response_model=List[LoanStatusResponse],
  status_code=HTTP_200_OK,
  summary="Listar estados de préstamo",
  description="Obtiene lista completa de estados de préstamo ordenada por ID",
)
async def get_all_loan_status(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all(db)
  return res
