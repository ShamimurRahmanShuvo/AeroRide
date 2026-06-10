from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import Base, TimestampMixin, UUIDMixin


class DriverAvailability(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "driver_availability"

    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), nullable=False)
    start_time: Mapped[DateTime] = mapped_column(nullable=True)
    end_time: Mapped[DateTime] = mapped_column(nullable=True)
    is_available: Mapped[bool] = mapped_column(default=True)

    driver = relationship("Driver", back_populates="availability_slots")
