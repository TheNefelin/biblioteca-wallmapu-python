from pydantic import BaseModel, ConfigDict


class EditionFormatDTO(BaseModel):
  id_edition: int
  id_format: int

  model_config = ConfigDict(from_attributes=True)
