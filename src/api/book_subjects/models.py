from sqlalchemy import Column, DateTime, Integer, String, func
from src.core.database import Base


class Subject(Base):
  __tablename__ = "wm_subjects"

  id_subject = Column(Integer, primary_key=True, autoincrement=True)
  subject = Column(String(200), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

