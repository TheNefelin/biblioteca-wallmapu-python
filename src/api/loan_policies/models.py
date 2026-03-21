from sqlalchemy import Column, Integer, String, Numeric

from src.core.database import Base


class LoanPolicy(Base):
  __tablename__ = "wm_loan_policies"

  id_policy = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100))
  max_books = Column(Integer)
  max_days = Column(Integer)
  fine_per_day = Column(Numeric(10, 2))
  reservation_days = Column(Integer, default=3)
