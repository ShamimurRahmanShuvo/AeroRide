from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.models.aero_enums import UserRole
from app.schemas.aero_base_schema import TimestampSchema


class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class UserResponseSchema(TimestampSchema):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    is_verified: bool
