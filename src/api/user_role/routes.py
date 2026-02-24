from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.shared.dtos import ApiResponse
from src.core.database import get_db
from . import repository, dtos

router = APIRouter(prefix="/user-role", tags=["user-role"])

# -----------------------------------------------------------------
# GET ALL 
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.UserRoleDTO]],
  status_code=HTTP_200_OK
)
def get_all_role(db: Session = Depends(get_db)):
  res = repository.get_all(db)
  return ApiResponse.success(data=res)
