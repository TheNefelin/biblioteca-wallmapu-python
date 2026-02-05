
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.news import dtos, repository
from src.shared.dtos import PaginationResponseDTO
from src.core.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=PaginationResponseDTO[List[dtos.NewsWithGalleryDTO]])
def get_all_pagination(
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
    
    # Construir URLs next/prev
    base_url = "/news"
    search_param = f"&search={search}" if search else ""
    
    next_url = None
    prev_url = None
    
    if page < pages:
      next_url = f"{base_url}?page={page + 1}&page_size={page_size}{search_param}"
    
    if page > 1:
      prev_url = f"{base_url}?page={page - 1}&page_size={page_size}{search_param}"
    
    return PaginationResponseDTO(
      count=count,
      pages=pages,
      next=next_url,
      prev=prev_url,
      result=result
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error: {str(e)}"
    )

@router.get("/all", response_model=List[dtos.NewsDTO])
def get_all(db: Session = Depends(get_db)):
  res = repository.get_all(db)
  return res

@router.get("/{id}", response_model=dtos.NewsDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
  res = repository.get_by_id(db, id)
  if not res:
    raise HTTPException(status_code=404, detail="Noticia no encontrado")
  return res
  
@router.post("/", response_model=dtos.NewsDTO, status_code=status.HTTP_201_CREATED)
def create(news: dtos.CreateNewsDTO, db: Session = Depends(get_db)):
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

@router.put("/{id}", response_model=dtos.NewsDTO)
def update(id: int, news: dtos.UpdateNewsDTO, db: Session = Depends(get_db)):
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