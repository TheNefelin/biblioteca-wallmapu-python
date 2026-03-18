from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/book-author", 
  tags=["book-author"], 
  dependencies=[admin_required]
)

# -----------------------------------------------------------------
# UPDATE (reemplaza autores del libro; body vacío elimina todos)
@router.put(
  "/{id_book}",
  response_model=ApiResponse[list[dtos.BookAuthorDTO]],
  status_code=HTTP_201_CREATED
)
def update_book_author(
  id_book: int,
  author_ids: list[int] = Body(..., embed=False),
  db: Session = Depends(get_db)
):
  try:
    res = service.update_authors(id_book, author_ids, db)
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
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
    res = service.delete_author(id_book, id_author, db)
    if not res:
      return ApiResponse.not_found()
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
