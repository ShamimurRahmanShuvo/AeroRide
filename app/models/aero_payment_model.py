from sqlalchemy import ForeignKey, Numeric, Enum, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.aero_base_model import Base, UUIDMixin, TimestampMixin
from app.models.aero_enums import PaymentStatus


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"

    booking_id: Mapped[str] = mapped_column(ForeignKey("bookings.id"), nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="CAD")
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    booking = relationship("Booking", back_populates="payment")
