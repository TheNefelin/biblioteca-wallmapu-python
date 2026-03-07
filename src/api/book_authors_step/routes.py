from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, repository

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/book-author", tags=["book-author"], dependencies=[admin_required])

# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id_book}",
  response_model=ApiResponse[list[dtos.BookAuthorDTO]],
  status_code=HTTP_201_CREATED
)
def update_book_author(
  id_book: int,
  author_ids: list[int],
  db: Session = Depends(get_db)
):
  try:
    res = repository.update(id_book, author_ids, db)

    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
    
# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_book}/{id_author}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK
)
def delete_book_author(
  id_book: int,
  id_author: int, 
  db: Session = Depends(get_db)
):
  try:
    item = dtos.BookAuthorDTO(
      id_book=id_book,
      id_author=id_author
    )

    res = repository.delete(item, db)

    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
