from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, service

router = APIRouter(
  prefix="/loan-status",
  tags=["loan-status"],
)

@router.get(
  "/",
  response_model=ApiResponse[List[dtos.LoanStatusDTO]],
  status_code=HTTP_200_OK,
  summary="Listar estados de préstamo",
  description="Obtiene lista completa de estados de préstamo ordenada por ID",
)
def get_all_loan_status(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))
