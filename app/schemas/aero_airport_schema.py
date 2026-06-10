from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class AeroAirportRegisterSchema(BaseModel):
    id: int
    name: str
    code: str
    city: str
    country: str
    timezone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AeroAirportResponseSchema(BaseModel):
    name: str
    code: str
    city: str
    country: str
    timezone: str

    class Config:
        from_attributes = True
    
