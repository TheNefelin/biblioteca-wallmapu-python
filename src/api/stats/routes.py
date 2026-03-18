
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/stat", tags=["stat"], dependencies=[admin_required])

# -----------------------------------------------------------------
# GET ALL 
@router.get(
  "/admin", 
  response_model=ApiResponse[dtos.StatusAdminDTO],
  status_code=HTTP_200_OK
)
def get_all_status_admin(db: Session = Depends(get_db)):
  res = service.get_all_admin(db)
  return ApiResponse.success(data=res)