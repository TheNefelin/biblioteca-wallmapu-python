from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/copy", tags=["copy"])


# -----------------------------------------------------------------
@router.get(
  "/detail/edition/{id_edition}",
  response_model=ApiResponse[List[dtos.CopyDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar ejemplares con detalle completo por edición",
  description="Retorna todos los ejemplares de una edición con datos de estado, libro, género y autor",
  dependencies=[admin_required],
)
def get_all_copy_detail_by_edition(id_edition: int, db: Session = Depends(get_db)):
  try:
    res = service.get_all_detail_by_edition_id(db, id_edition)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.get(
  "/detail/book/{id_book}",
  response_model=ApiResponse[List[dtos.CopyDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar ejemplares con detalle completo por libro",
  description="Retorna todos los ejemplares de un libro con datos de estado, edición, género y autor",
)
def get_all_copy_detail_by_book(id_book: int, db: Session = Depends(get_db)):
  try:
    res = service.get_all_detail_by_book_id(db, id_book)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.post(
  "/",
  response_model=ApiResponse[dtos.CopyDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear nuevo ejemplar",
  description="Crea un nuevo ejemplar asociado a una edición",
  dependencies=[admin_required],
)
def create_copy(copy: dtos.CreateCopyDTO, db: Session = Depends(get_db)):
  try:
    res = service.create(db, copy)
    return ApiResponse.created(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.CopyDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar ejemplar",
  description="Actualiza un ejemplar existente por ID",
  dependencies=[admin_required],
)
def update_copy(id: int, copy: dtos.UpdateCopyDTO, db: Session = Depends(get_db)):
  try:
    res = service.update(db, id, copy)
    if not res:
      return ApiResponse.not_found(message="Ejemplar no encontrado")
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar ejemplar",
  description="Elimina un ejemplar por ID",
  dependencies=[admin_required],
)
def delete_copy(id: int, db: Session = Depends(get_db)):
  try:
    res = service.delete(db, id)
    if not res:
      return ApiResponse.not_found(message="Ejemplar no encontrado")
    return ApiResponse.success(data=res, message="Ejemplar eliminado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))




