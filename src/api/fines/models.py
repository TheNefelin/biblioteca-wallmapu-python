from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Fine(Base):
  __tablename__ = "wm_fines"

  id_fine = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(Numeric(10, 2), nullable=False)
  reason = Column(String(255))
  paid = Column(Boolean, default=False)
  created_at = Column(DateTime, server_default=func.now())

  loan_id = Column(Integer, ForeignKey("wm_loans.id_loan"), nullable=False)

  loan = relationship("Loan", back_populates="fines")
