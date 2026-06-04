from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class RegisterUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password_hash: str = Field(..., min_length=8)
    roles: Optional[List[str]] = ["user"]


class LoginUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class UserProfileSchema(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        orm_mode = True


class CurrentUserResponseSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    is_active: bool
    is_varified: bool
    created_at: datetime
    updated_at: datetime
    roles: List[str]
    profile: Optional[UserProfileSchema] = None


class RoleResponseSchema(BaseModel):
    id: int
    name: str


class RoleRequestSchema(BaseModel):
    role_name: str = Field(..., min_length=3, max_length=50)


class UserRoleAssignmentSchema(BaseModel):
    user_id: int
    role_id: int
