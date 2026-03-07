from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, repository

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/book-subject", tags=["book-subject"], dependencies=[admin_required])

# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_book}/{id_subject}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK
)
def delete_subject(
  id_book: int,
  id_subject: int, 
  db: Session = Depends(get_db)
):
  try:
    item = dtos.BookSubjectDTO(
      id_book=id_book,
      id_subject=id_subject
    )

    res = repository.delete(item, db)

    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))
