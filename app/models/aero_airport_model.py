from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.aero_base_model import Base, UUIDMixin, TimestampMixin


class Airport(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "airports"

    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

    bookings = relationship("Booking", back_populates="airport")
