
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from src.api.news import repository
from src.api.news.dtos import CreateNewsDTO, NewsDTO, NewsWithGalleryDTO, UpdateNewsDTO
from src.core.url_helper import get_base_url, get_static_news_url
from src.shared.dtos import ApiResponse, PaginationResponseDTO
from src.core.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=ApiResponse[PaginationResponseDTO[List[NewsWithGalleryDTO]]])
def get_all_pagination(
  request: Request,
  page: int = Query(default=1, ge=1, description="Número de página"),
  page_size: int = Query(default=10, ge=1, le=100, description="Elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar en título o subtítulo"),
  db: Session = Depends(get_db)
):
  try:
    count, pages, result = repository.get_all_pagination(page, page_size, search, db)
    
    # Ajuste automático de página
    if page > pages and pages > 0:
      page = pages
      count, pages, result = repository.get_all_pagination(page, page_size, search, db)
    
    base_url = get_base_url(request)
    static_url = get_static_news_url(request)

    # Construir URLs next/prev
    search_param = f"&search={search}" if search else ""
    
    next_url = None
    prev_url = None
    
    if page < pages:
      next_url = f"{base_url}?page={page + 1}&page_size={page_size}{search_param}"
    
    if page > 1:
      prev_url = f"{base_url}?page={page - 1}&page_size={page_size}{search_param}"
    
    # Añadir base_url a las imágenes de cada noticia
    for news in result:
      for image in news.images:
        image.img = f"{static_url}/{image.img}"

    paginationResult = PaginationResponseDTO(  
      count=count,
      pages=pages,
      next=next_url,
      prev=prev_url,
      result=result
    )

    return ApiResponse.success(paginationResult)
  except Exception as e:
    return ApiResponse.server_error(str(e))
    #raise HTTPException(
    #  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #  detail=f"Error: {str(e)}"
    #)

@router.get("/{id}", response_model=ApiResponse[NewsWithGalleryDTO])
def get_by_id(
  request: Request,
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    result = repository.get_by_id(id, db)

    if result:
      static_url = get_static_news_url(request)

      for image in result.images:
        image.img = f"{static_url}/{image.img}"
    else:
      return ApiResponse.not_found()
    return ApiResponse.success(result)  
  except Exception as e:
    return ApiResponse.server_error(str(e))
  






@router.post("/", response_model=NewsDTO, status_code=status.HTTP_201_CREATED)
def create(news: CreateNewsDTO, db: Session = Depends(get_db)):
  try:
    created = repository.create(db, news)

    return created
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error interno del servidor: {e}"
    )

@router.put("/{id}", response_model=NewsDTO)
def update(id: int, news: UpdateNewsDTO, db: Session = Depends(get_db)):
  try:
    updated = repository.update(db, id, news)
    
    if not updated:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Noticia con id {id} no encontrado"
      )
    
    return updated
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Error interno del servidor"
    )