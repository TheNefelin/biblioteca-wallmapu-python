from typing import Generic, Optional, TypeVar
from fastapi import status
from pydantic import BaseModel

T = TypeVar('T')

class PaginationResponseDTO(BaseModel, Generic[T]): 
  count: int
  pages: int
  next: Optional[str] = None
  prev: Optional[str] = None
  result: T

class ApiResponse(BaseModel, Generic[T]):
  isSuccess: bool
  statusCode: int
  message: str
  data: Optional[T] 

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
  def updated(cls, data: Optional[T] = None, message: str = "Recurso actualizado") -> 'ApiResponse[T]':
    return cls(
      isSuccess=True, 
      statusCode=status.HTTP_200_OK, 
      message=message, 
      data=data
    )

  @classmethod
  def deleted(cls, message: str = "Recurso eliminado") -> 'ApiResponse[T]':
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
  def custom(cls, status_code: int, is_success: bool, message: str, data: Optional[T] = None) -> 'ApiResponse[T]':
    return cls(
      isSuccess=is_success, 
      statusCode=status_code, 
      message=message, 
      data=data
    )

  