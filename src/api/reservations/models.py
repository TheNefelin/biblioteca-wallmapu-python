from sqlalchemy import Column, Integer, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Reservation(Base):
  __tablename__ = "wm_reservations"

  id_reservation = Column(Integer, primary_key=True, autoincrement=True)
  reservation_date = Column(DateTime, server_default=func.now())
  expiration_date = Column(DateTime, nullable=False)

  user_id = Column(UUID(as_uuid=True), ForeignKey("wm_users.id_user"), nullable=False)
  copy_id = Column(Integer, ForeignKey("wm_copies.id_copy"), nullable=False)
  reservation_status_id = Column(Integer, ForeignKey("wm_reservation_status.id_status"), nullable=False, default=1)

  user = relationship("User", back_populates="reservations")
  copy = relationship("Copy", back_populates="reservations")
  status = relationship("ReservationStatus")
