from pydantic import BaseModel, ConfigDict


class BookAuthorDTO(BaseModel):
  id_book: int
  id_author: int

  model_config = ConfigDict(from_attributes=True)