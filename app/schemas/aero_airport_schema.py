from pydantic import BaseModel, Field
from .aero_base_schema import TimestampSchema


class AirportCreateSchema(BaseModel):
    name: str = Field(..., example="John F. Kennedy International Airport")
    code: str = Field(..., example="JFK")
    city: str = Field(..., example="New York")
    country: str = Field(..., example="USA")


class AirportResponseSchema(TimestampSchema):
    name: str = Field(..., example="John F. Kennedy International Airport")
    code: str = Field(..., example="JFK")
    city: str = Field(..., example="New York")
    country: str = Field(..., example="USA")
