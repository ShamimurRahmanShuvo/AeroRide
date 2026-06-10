from datetime import datetime
from pydantic import BaseModel, Field
from .aero_base_schema import TimestampSchema


class DriverAvailabilityCreateSchema(BaseModel):
    driver_id: int = Field(..., description="ID of the driver")
    available_from: datetime = Field(..., description="Start time of availability")
    available_to: datetime = Field(..., description="End time of availability")
    is_available: bool = Field(..., description="Whether the availability is active")


class DriverAvailabilityResponseSchema(TimestampSchema):
    driver_id: int = Field(..., description="ID of the driver")
    available_from: datetime = Field(..., description="Start time of availability")
    available_to: datetime = Field(..., description="End time of availability")
    is_available: bool = Field(..., description="Whether the availability is active")
