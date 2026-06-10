from pydantic import BaseModel, Field
from .aero_base_schema import TimestampSchema


class DriverCreateSchema(BaseModel):
    user_id: str = Field(..., description="ID of the associated user")
    license_number: str = Field(..., description="Driver's license number")


class DriverResponseSchema(TimestampSchema):
    user_id: str = Field(..., description="ID of the associated user")
    license_number: str = Field(..., description="Driver's license number")
    rating: float = Field(..., description="Driver's average rating")
    is_active: bool = Field(..., description="Driver's active status")
