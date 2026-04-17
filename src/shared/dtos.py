from typing import Generic, Optional, TypeVar
from fastapi import status
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginationRequestDTO(BaseModel):
  page: int 
  limit: int 
  search: Optional[str] = None

class BookPaginationRequestDTO(BaseModel):
  page: int 
  limit: int 
  search: Optional[str] = None
  id_author: Optional[int]
  id_editorial: Optional[int]
  id_genre: Optional[int]

class PaginationResponseDTO(BaseModel, Generic[T]): 
  page: int = Field(..., description="Página actual")
  pages: int= Field(..., description="Cantidad total de páginas disponibles")
  items: int = Field(..., description="Cantidad total de registros disponibles")
  next: Optional[str] = Field(None, description="URL de la siguiente página, si existe")
  prev: Optional[str] = Field(None, description="URL de la página anterior, si existe")
  data: Optional[T] = Field(None, description="Lista de resultados de la página actual")

class ApiResponse(BaseModel, Generic[T]):
  isSuccess: bool = Field(..., description="Indica si la operación fue exitosa")
  statusCode: int = Field(..., description="Código HTTP de la respuesta")
  message: str = Field(..., description="Mensaje descriptivo de la operación")
  data: Optional[T] = Field(None, description="Datos devueltos por la operación")

  @classmethod
  def success(cls, data: Optional[T] = None, message: str = "Operación exitosa") -> 'ApiResponse[T]':
    return cls(
      isSuccess=True, 
      statusCode=status.HTTP_200_OK, 
      message=message, 
      data=data
    )  

  @classmethod
  def created(cls, data: Optional[T] = None, message: str = "Recurso creado") -> 'ApiResponse[T]':
    return cls(
      isSuccess=True, 
      statusCode=status.HTTP_201_CREATED, 
      message=message, 
      data=data
    )

  @classmethod
  def deleted(cls, data: Optional[T] = None, message: str = "Recurso eliminado") -> 'ApiResponse[T]':
    return cls(
      isSuccess=True, 
      statusCode=status.HTTP_204_NO_CONTENT, 
      message=message, 
      data=None
    )

  @classmethod
  def not_found(cls, message: str = "Recurso no encontrado") -> 'ApiResponse[T]':
    return cls(
      isSuccess=False, 
      statusCode=status.HTTP_404_NOT_FOUND, 
      message=message, 
      data=None
    )

  @classmethod
  def bad_request(cls, message: str = "Solicitud inválida") -> 'ApiResponse[T]':
    return cls(
      isSuccess=False, 
      statusCode=status.HTTP_400_BAD_REQUEST, 
      message=message, 
      data=None
    )

  @classmethod
  def server_error(cls, message: str = "Error interno del servidor") -> 'ApiResponse[T]':
    return cls(
      isSuccess=False, 
      statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR, 
      message=message, 
      data=None
    )

  @classmethod
  def unauthorized(cls, message: str = "No autorizado") -> 'ApiResponse[T]':
    return cls(
      isSuccess=False,
      statusCode=status.HTTP_401_UNAUTHORIZED,
      message=message,
      data=None
    )

  @classmethod
  def forbidden(cls, message: str = "Acceso prohibido") -> 'ApiResponse[T]':
    return cls(
      isSuccess=False,
      statusCode=status.HTTP_403_FORBIDDEN,
      message=message,
      data=None
    )
