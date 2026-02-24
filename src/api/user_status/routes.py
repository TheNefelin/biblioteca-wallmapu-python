from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.core.roles import UserRole
from src.core.jwt_service import get_current_user
from src.api.user_status.dtos import UserStatusDTO
from src.api.user_status.repository import get_all
from src.shared.dtos import ApiResponse

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/user-status", tags=["user-status"], dependencies=[admin_or_user_required])

# -----------------------------------------------------------------
# GET ALL 
@router.get(
  "/", 
  response_model=ApiResponse[List[UserStatusDTO]],
  status_code=HTTP_200_OK
)
def get_all_status(db: Session = Depends(get_db)):
  res = get_all(db)
  return ApiResponse.success(data=res)
