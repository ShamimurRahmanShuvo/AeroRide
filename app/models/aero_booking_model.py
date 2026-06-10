from sqlalchemy import Enum, ForeignKey, String, Float, Integer, Text, Numeric, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.aero_base_model import Base, UUIDMixin, TimestampMixin
from app.models.aero_enums import BookingStatus


class Booking(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bookings"

    customer_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    driver_id: Mapped[str] = mapped_column(ForeignKey("drivers.id"), nullable=True)
    airport_id: Mapped[str] = mapped_column(ForeignKey("airports.id"), nullable=False)

    pickup_address: Mapped[str] = mapped_column(Text)
    dropoff_address: Mapped[str] = mapped_column(Text)

    flight_number: Mapped[str] = mapped_column(Text)
    pickup_time: Mapped[str] = mapped_column(Text)
    passenger_count: Mapped[int] = mapped_column(Integer)
    luggage_count: Mapped[int] = mapped_column(Integer)
    distance_km: Mapped[float] = mapped_column(Numeric(10, 2))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.PENDING)

    rider = relationship("User", foreign_keys=[customer_id], back_populates="customer_bookings")
    driver = relationship("Driver", foreign_keys=[driver_id], back_populates="bookings")
    airport = relationship("Airport", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)
    status_history = relationship("BookingStatusHistory",
                                  back_populates="booking", cascade="all, delete-orphan")
