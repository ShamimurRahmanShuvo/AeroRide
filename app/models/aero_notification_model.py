from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import Base, TimestampMixin, UUIDMixin
from app.models.aero_enums import NotificationChannel


class Notification(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    channel: Mapped[NotificationChannel] = mapped_column(Enum(NotificationChannel), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")

    user = relationship("User", back_populates="notifications")
