from pydantic import BaseModel, Field
from app.models.aero_enums import VehicleType
from .aero_base_schema import TimestampSchema
from .aero_driver_schema import DriverResponseSchema


class VehicleCreateSchema(BaseModel):
    driver_id: int = Field(..., description="ID of the driver associated with the vehicle")
    make: str = Field(..., description="Make of the vehicle")
    model: str = Field(..., description="Model of the vehicle")
    year: int = Field(..., description="Year of manufacture of the vehicle")
    license_plate: str = Field(..., description="License plate number of the vehicle")
    color: str = Field(..., description="Color of the vehicle")
    capacity: int = Field(..., description="Seating capacity of the vehicle")
    vehicle_type: VehicleType = Field(..., description="Type of the vehicle (e.g., Car, Van, SUV)")


class VehicleResponseSchema(TimestampSchema):
    driver_id: int = Field(..., description="ID of the driver associated with the vehicle")
    make: str = Field(..., description="Make of the vehicle")
    model: str = Field(..., description="Model of the vehicle")
    year: int = Field(..., description="Year of manufacture of the vehicle")
    license_plate: str = Field(..., description="License plate number of the vehicle")
    color: str = Field(..., description="Color of the vehicle")
    capacity: int = Field(..., description="Seating capacity of the vehicle")
    vehicle_type: VehicleType = Field(..., description="Type of the vehicle (e.g., Car, Van, SUV)")


class VehicleDetailResponseSchema(VehicleResponseSchema):
    driver: DriverResponseSchema = Field(..., description="Details of the driver associated with the vehicle")
