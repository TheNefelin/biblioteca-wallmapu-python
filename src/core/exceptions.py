from fastapi import status
from rfc9457 import BadRequestProblem, ForbiddenProblem, NotFoundProblem, Problem, UnauthorisedProblem


class AppError(Problem):
  """Error de negocio base (RFC 9457/Problem Details).

  Se serializa como `{type, title, status, detail}` y el handler global de
  `main.py` (fastapi-problem) lo convierte a una respuesta problem+json.
  """

  def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    self.message = message
    super().__init__(title=message, detail=message, status=status_code, type_="app-error")


class NotFoundError(NotFoundProblem):
  type_ = "not-found"
  title = "Resource not found."

  def __init__(self, entity: str = "Recurso"):
    super().__init__(detail=f"{entity} no encontrado")
    self.message = self.detail


class DuplicateNameError(BadRequestProblem):
  type_ = "duplicate-name"
  title = "Duplicate resource."

  def __init__(self, name: str):
    super().__init__(detail=f"Ya existe un registro con el nombre '{name}'")
    self.message = self.detail


class UnauthorizedError(UnauthorisedProblem):
  type_ = "unauthorized"
  title = "Unauthorized."

  def __init__(self, message: str = "Token inválido o expirado"):
    super().__init__(detail=message)
    self.message = message


class ForbiddenError(ForbiddenProblem):
  type_ = "forbidden"
  title = "Forbidden."

  def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
    super().__init__(detail=message)
    self.message = message
