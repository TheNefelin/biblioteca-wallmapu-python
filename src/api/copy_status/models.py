from sqlalchemy import Column, Integer, String

from src.core.database import Base


class CopyStatus(Base):
  __tablename__ = "wm_copy_status"

  id_status = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(45), nullable=False)
