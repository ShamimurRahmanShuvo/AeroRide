from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class AeroUser(Base):
    __tablename__ = "aero_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
    is_varified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = relationship("UserRole", back_populates="users")
    profiles = relationship("UserProfile", back_populates="user", uselist=False)


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
