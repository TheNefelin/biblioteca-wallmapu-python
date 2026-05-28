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
  status_code=HTTP_201_CREATED,
  summary="Reemplazar autores de un libro",
  description="Elimina todos los autores actuales y asigna la nueva lista. Body vacío elimina todos.",
)
def update_book_author(
  id_book: int,
  author_ids: list[int] = Body(..., embed=False),
  db: Session = Depends(get_db)
):
  try:
    res = service.update_authors(db, id_book, author_ids)
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
  status_code=HTTP_200_OK,
  summary="Eliminar un autor de un libro",
  description="Elimina la relación autor-libro específica",
)
def delete_book_author(
  id_book: int,
  id_author: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete_author(db, id_book, id_author)
    if not res:
      return ApiResponse.not_found()
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE BY ID BOOK
@router.delete(
  "/book/{id_book}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar todos los autores de un libro",
  description="Elimina todas las relaciones de autor para un libro específico",
)
def delete_book_author_by_book(
  id_book: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete_author_by_book(db, id_book)
    if not res:
      return ApiResponse.not_found()
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

