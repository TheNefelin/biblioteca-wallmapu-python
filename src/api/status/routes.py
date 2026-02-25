
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, repository

router = APIRouter(prefix="/status", tags=["status"])

# -----------------------------------------------------------------
# GET ALL 
@router.get(
  "/admin", 
  response_model=ApiResponse[dtos.StatusAdminDTO],
  status_code=HTTP_200_OK
)
def get_all_status_admin(db: Session = Depends(get_db)):
  res = repository.get_all_admin(db)
  return ApiResponse.success(data=res)