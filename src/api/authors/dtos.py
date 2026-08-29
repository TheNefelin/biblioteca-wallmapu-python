from src.schemas.dtos import AuthorRequest, AuthorResponse

CreateAuthorDTO = AuthorRequest
UpdateAuthorDTO = AuthorRequest
AuthorDTO = AuthorResponse

__all__ = ["CreateAuthorDTO", "UpdateAuthorDTO", "AuthorDTO", "AuthorRequest", "AuthorResponse"]
