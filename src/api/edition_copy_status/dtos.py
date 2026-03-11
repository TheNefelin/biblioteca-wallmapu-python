from pydantic import BaseModel, ConfigDict


class CopyStatusDTO(BaseModel):
  id_status: int
  name: str

  model_config = ConfigDict(from_attributes=True)