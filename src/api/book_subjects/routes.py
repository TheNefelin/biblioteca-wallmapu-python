from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.exceptions import AppError, NotFoundError
from src.schemas.dtos import BookSubjectResponse
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/book-subject",
  tags=["book-subject"],
  dependencies=[admin_required]
)

# -----------------------------------------------------------------
# UPDATE (reemplaza descriptores del libro; body vacío elimina todos)
@router.put(
  "/{id_book}",
  response_model=list[BookSubjectResponse],
  status_code=HTTP_200_OK,
  summary="Reemplazar descriptores de un libro",
  description="Elimina todos los descriptores actuales y asigna la nueva lista. Body vacío elimina todos.",
)
async def update_book_subject(
  id_book: int,
  subject_ids: list[int] = Body(..., embed=False),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.update_subjects(db, id_book, subject_ids)
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_book}/{id_subject}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar un descriptor de un libro",
  description="Elimina la relación descriptor-libro específica",
)
async def delete_book_subject(
  id_book: int,
  id_subject: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete_subject(db, id_book, id_subject)
    if not res:
      raise NotFoundError()
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
# DELETE BY ID BOOK
@router.delete(
  "/book/{id_book}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar todos los descriptores de un libro",
  description="Elimina todas las relaciones de descriptor para un libro específico",
)
async def delete_book_subject_by_book(
  id_book: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete_subject_by_book(db, id_book)
    if not res:
      raise NotFoundError()
    return res
  except ValueError as e:
    raise AppError(str(e))