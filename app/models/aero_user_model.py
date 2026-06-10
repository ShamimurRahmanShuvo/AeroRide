from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import AeroBaseModel, TimestampMixin, UUIDMixin
from app.models.aero_enums import UserRole
# from app.core.database import Base


class AeroUser(UUIDMixin, TimestampMixin, AeroBaseModel):
    __tablename__ = "aero_users"

    # id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False)

    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
    rider_bookings = relationship("Booking", back_populates="rider", foreign_keys="Booking.rider_id")
    notifications = relationship("Notification", back_populates="user")


"""
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, nullable=False)

    users = relationship("UserRole", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='unique_user_role'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("aero_users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    users = relationship("AeroUser", back_populates="roles")
    roles = relationship("Role", back_populates="users")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("aero_users.id"), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone_number = Column(String(20), nullable=True)

    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    profile_picture_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("AeroUser", back_populates="profiles")
"""