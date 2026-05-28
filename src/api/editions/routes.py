from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/edition", tags=["edition"])


# -----------------------------------------------------------------
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.EditionDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar ediciones con paginación (DTO plano)",
  description="Retorna lista paginada con DTO plano. Filtros: id_author, id_editorial, id_genre, id_format, id_subject, search",
)
def get_all_pagination(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: Optional[str] = Query(default=""),
  id_author: Optional[int] = Query(default=None),
  id_editorial: Optional[int] = Query(default=None),
  id_genre: Optional[int] = Query(default=None),
  id_format: Optional[int] = Query(default=None),
  id_subject: Optional[int] = Query(default=None),
  db: Session = Depends(get_db)
):
  try:
    filter = dtos.EditionFilterDTO(
      id_author=id_author,
      id_editorial=id_editorial,
      id_genre=id_genre,
      id_format=id_format,
      id_subject=id_subject
    ) if any([id_author, id_editorial, id_genre, id_format, id_subject]) else None

    pagination = PaginationRequestDTO[dtos.EditionFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = service.get_all_pagination(db, pagination)

    if pagination_response.pages > pagination_response.page:
      pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
    if pagination_response.page > 1:
      pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.get(
  "/book/{id_book}/detail",
  response_model=ApiResponse[List[dtos.EditionDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar ediciones por libro con detalle",
  description="Retorna todas las ediciones de un libro con DTO plano (editorial, género, autor, copy_count)",
  dependencies=[admin_required],
)
def get_editions_by_book_detail(id_book: int, db: Session = Depends(get_db)):
  try:
    res = service.get_all_by_book_id_detail(db, id_book)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.get(
  "/book/{id_book}",
  response_model=ApiResponse[List[dtos.EditionDTO]],
  status_code=HTTP_200_OK,
  summary="Listar ediciones por libro",
  description="Retorna todas las ediciones de un libro (básico, sin relaciones)",
)
def get_editions_by_book(id_book: int, db: Session = Depends(get_db)):
  try:
    res = service.get_by_book_id(db, id_book)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.EditionDTO],
  status_code=HTTP_200_OK,
  summary="Obtener edición básica por ID",
  description="Retorna una edición sin relaciones",
  dependencies=[admin_required],
)
def get_edition_by_id(id: int, db: Session = Depends(get_db)):
  try:
    res = service.get_edition_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Edición no encontrada")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.post(
  "/",
  response_model=ApiResponse[dtos.EditionDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear nueva edición",
  description="Crea una nueva edición asociada a un libro",
  dependencies=[admin_required],
)
def create_edition(item: dtos.CreateEditionDTO, db: Session = Depends(get_db)):
  try:
    res = service.create_edition(db, item)
    return ApiResponse.created(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.EditionDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar edición",
  description="Actualiza una edición existente por ID",
  dependencies=[admin_required],
)
def update_edition(id: int, item: dtos.UpdateEditionDTO, db: Session = Depends(get_db)):
  try:
    result = service.update_edition(db, id, item)
    if not result:
      return ApiResponse.not_found(message="Edición no encontrada")
    return ApiResponse.success(data=result)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar edición",
  description="Elimina una edición y su imagen de Cloudinary (si tiene)",
  dependencies=[admin_required],
)
def delete_edition(id: int, db: Session = Depends(get_db)):
  try:
    res = service.delete_edition_with_image(db, id)
    if not res:
      return ApiResponse.not_found(message="Edición no encontrada")
    return ApiResponse.success(data=res, message="Edición eliminada exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))
