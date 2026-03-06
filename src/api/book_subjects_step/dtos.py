from pydantic import BaseModel, ConfigDict


class BookSubjectDTO(BaseModel):
  id_subject: int
  id_book: int

  model_config = ConfigDict(from_attributes=True)