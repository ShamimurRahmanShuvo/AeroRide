from sqlalchemy import ForeignKey, Float, Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import Base, TimestampMixin, UUIDMixin


class Driver(Base, UUIDMixin, TimestampMixin):
    __tablename__ = 'drivers'

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="driver_profile")
    vehicles = relationship("Vehicle", back_populates="driver", uselist=False)
    bookings = relationship("Booking", back_populates="driver")
    availability_slots = relationship("DriverAvailability", back_populates="driver")
    documents = relationship("DriverDocument", back_populates="driver")
