from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/edition-image", 
  tags=["edition-image"],
  dependencies=[admin_required],
)

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[str],
  status_code=status.HTTP_201_CREATED
)
def create_edition_image(
  file: UploadFile = File(...),
):
  try:
    url = service.create_edition_image(
      file=file,
    )

    return ApiResponse.created(data=url)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
    
# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_edition}", 
  response_model=ApiResponse[bool],
  status_code=status.HTTP_200_OK
)
def delete_edition_image(
  id_edition: int,
  db: Session = Depends(get_db)
):
  try:
    result = service.delete_edition_image(id_edition, db)
  
    return ApiResponse.success(data=result)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
