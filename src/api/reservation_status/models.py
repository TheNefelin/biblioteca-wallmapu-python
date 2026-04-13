from sqlalchemy import Column, Integer, String

from src.core.database import Base


class ReservationStatus(Base):
  __tablename__ = "wm_reservation_status"

  id_status = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(30), nullable=False)
