from pydantic import BaseModel, ConfigDict


class BookSubjectDTO(BaseModel):
  id_book: int
  id_subject: int

  model_config = ConfigDict(from_attributes=True)