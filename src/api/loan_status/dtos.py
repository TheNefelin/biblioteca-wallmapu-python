from pydantic import BaseModel, ConfigDict


class LoanStatusDTO(BaseModel):
  id_status: int
  status: str
  
  model_config = ConfigDict(from_attributes=True)
