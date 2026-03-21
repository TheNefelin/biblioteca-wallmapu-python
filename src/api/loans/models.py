from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base
from src.api.loan_status.models import LoanStatus


class Loan(Base):
  __tablename__ = "wm_loans"

  id_loan = Column(Integer, primary_key=True, autoincrement=True)
  loan_date = Column(Date, server_default=func.current_date(), nullable=False)
  due_date = Column(Date, nullable=False)
  return_date = Column(Date, nullable=True)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  copy_id = Column(Integer, ForeignKey("wm_copies.id_copy"), nullable=False)
  user_id = Column(String(36), ForeignKey("wm_users.id_user"), nullable=False)
  loan_status_id = Column(Integer, ForeignKey("wm_loan_status.id_status"), nullable=False, default=1)

  copy = relationship("Copy")
  user = relationship("User")
  status = relationship("LoanStatus")
