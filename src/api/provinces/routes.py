from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, repository

router = APIRouter(prefix="/province", tags=["province"])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.ProvinceDTO]],
  status_code=HTTP_200_OK
)
def get_all_province(db: Session = Depends(get_db)):
  try:
    res = repository.get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))
