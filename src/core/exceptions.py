from fastapi import status


class AppError(Exception):
  """Error de aplicación con código HTTP asociado.

  Se captura en las routes para devolver la respuesta en el formato
  `ApiResponse`, manteniendo el contrato del frontend.
  """

  def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    self.message = message
    self.status_code = status_code
    super().__init__(message)


class NotFoundError(AppError):
  def __init__(self, entity: str = "Recurso"):
    super().__init__(
      message=f"{entity} no encontrado",
      status_code=status.HTTP_404_NOT_FOUND,
    )


class DuplicateNameError(AppError):
  def __init__(self, name: str):
    super().__init__(
      message=f"Ya existe un registro con el nombre '{name}'",
      status_code=status.HTTP_400_BAD_REQUEST,
    )


class UnauthorizedError(AppError):
  def __init__(self, message: str = "Token inválido o expirado"):
    super().__init__(
      message=message,
      status_code=status.HTTP_401_UNAUTHORIZED,
    )


class ForbiddenError(AppError):
  def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
    super().__init__(
      message=message,
      status_code=status.HTTP_403_FORBIDDEN,
    )
