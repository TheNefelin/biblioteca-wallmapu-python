
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.news import dtos, repository
from src.core.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=List[dtos.NewsDTO])
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