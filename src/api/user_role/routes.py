from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import repository, dtos

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/user-role", tags=["user-role"], dependencies=[admin_or_user_required])

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
