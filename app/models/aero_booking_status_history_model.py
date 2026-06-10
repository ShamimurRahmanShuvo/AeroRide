from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.aero_base_model import *
from app.models.aero_enums import BookingStatus


class BookingStatusHistory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "booking_status_history"

    booking_id: Mapped[str] = mapped_column(ForeignKey("aero_bookings.id"), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), nullable=False)
    changed_by: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "system", "rider", "driver"

    booking = relationship("Booking", back_populates="status_history")
