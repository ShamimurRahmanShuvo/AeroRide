from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import Base, UUIDMixin, TimestampMixin
from app.models.aero_enums import VehicleType


class Vehicle(Base, UUIDMixin, TimestampMixin):
    __tablename__ = 'vehicles'

    driver_id: Mapped[str] = mapped_column(ForeignKey("drivers.id"), nullable=False, unique=True)
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(30))
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    vehicle_type: Mapped[VehicleType] = mapped_column(Enum(VehicleType), nullable=False)

    driver = relationship("Driver", back_populates="vehicle")
