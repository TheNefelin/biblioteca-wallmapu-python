
import stat
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, session

from src.api.news_gallery import dtos, repository
from src.core.database import get_db

router = APIRouter(prefix="/news-gallery", tags=["news-gallery"])

@router.get("/", response_model=List[dtos.NewsGalleryDTO])
def get_all(db: Session = Depends(get_db)):
  res = repository.get_all(db)
  return res

@router.get("/{id}", response_model=dtos.NewsGalleryDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
  res = repository.get_by_id(db, id)
  
  if not res:
    raise HTTPException(status_code=404, detail="Imagen no encontrado")
  return res
  
@router.get("/by-news/{id}", response_model=List[dtos.NewsGalleryDTO])
def get_by_news_id(id: int, db: Session = Depends(get_db)):
  res = repository.get_by_news_id(db, id)
  return res

@router.post("/", response_model=dtos.NewsGalleryDTO, status_code=status.HTTP_201_CREATED)
def create(item: dtos.CreateGalleryDTO, db: Session = Depends(get_db)):
  try:
    created = repository.create(db, item)

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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
  repository.delete(db, id)
