from datetime import datetime

from pydantic import BaseModel, Field

from app.models.aero_enums import BookingStatus

from .aero_airport_schema import AirportResponseSchema
from .aero_driver_schema import DriverResponseSchema
from .aero_user_schema import UserResponseSchema
from .aero_base_schema import TimestampSchema


class BookingCreateSchema(BaseModel):
    customer_id: int = Field(..., example=1)
    airport_id: int = Field(..., example=1)
    pickup_address: str = Field(..., example="123 Main St, New York, NY")
    dropoff_address: str = Field(..., example="456 Elm St, New York, NY")
    flight_number: str = Field(..., example="AA123")
    pickup_time: datetime = Field(..., example="2024-07-01T15:30:00Z")
    passenger_count: int = Field(..., example=2)
    luggage_count: int = Field(..., example=3)


class BookingResponseSchema(TimestampSchema):
    id: int
    customer_id: int
    driver_id: int
    airport_id: int
    pickup_address: str
    dropoff_address: str
    flight_number: str
    pickup_time: datetime
    passenger_count: int
    luggage_count: int
    distance_km: float
    duration_minutes: int
    price: float
    status: BookingStatus


class BookingDetailResponseSchema(TimestampSchema):
    customer: UserResponseSchema
    driver: DriverResponseSchema
    airport: AirportResponseSchema
    pickup_address: str
    dropoff_address: str
    flight_number: str
    pickup_time: datetime
    passenger_count: int
    luggage_count: int
    distance_km: float
    duration_minutes: int
    price: float
    status: BookingStatus
