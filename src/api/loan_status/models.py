from sqlalchemy import Column, Integer, String

from src.core.database import Base


class LoanStatus(Base):
  __tablename__ = "wm_loan_status"

  id_status = Column(Integer, primary_key=True)
  status = Column(String(30), nullable=False)
