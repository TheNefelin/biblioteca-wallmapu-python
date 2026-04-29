from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/subject", 
  tags=["subject"], 
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.SubjectDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar descriptores con paginación",
  description="Obtiene lista paginada de descriptores, opcionalmente filtrada por búsqueda",
  dependencies=[admin_required]
)
def get_subjects_paginated(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  db: Session = Depends(get_db)
):
  try:
    pagination_request = PaginationRequestDTO[None](
      page=page,
      limit=limit,
      search=search or "",
      filter=None,
    )

    pagination_response = service.get_all_pagination(db, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=ApiResponse[List[dtos.SubjectDTO]],
  status_code=HTTP_200_OK,
  summary="Listar todos los descriptores",
  description="Obtiene lista completa de descriptores ordenada por nombre",
)
def get_all_subject(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[dtos.SubjectDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo Descriptor",
  description="Crea un descriptor con el nombre proporcionado",
  dependencies=[admin_required],
)
def create_subject(
  dto: dtos.CreateSubjectDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.create(db, dto)
    return ApiResponse.created(data=res, message="Descriptor creado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.SubjectDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar un Descriptor",
  description="Actualiza el nombre de un descriptor existente",
  dependencies=[admin_required],
)
def update_subject(
  id: int,
  dto: dtos.UpdateSubjectDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.update(db, id, dto)

    if not res:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res, message="Descriptor modificado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar un Descriptor",
  description="Elimina un descriptor. Falla si está asociado a libros",
  dependencies=[admin_required],  
)
def delete_subject(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete(db, id)

    if res is None:
      return ApiResponse.not_found()

    if res is False:
      return ApiResponse.bad_request(message="No se puede eliminar: descriptor tiene libros asociados")

    return ApiResponse.success(data=True, message="Descriptor eliminado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
