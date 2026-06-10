from pydantic import Field
from app.models.aero_enums import PaymentStatus
from .aero_base_schema import TimestampSchema


class PaymentResponseSchema(TimestampSchema):
    booking_id: str = Field(..., description="ID of the booking associated with the payment")
    amount: float = Field(..., description="Amount paid for the booking")
    currency: str = Field(..., description="Currency of the payment")
    status: PaymentStatus = Field(..., description="Status of the payment")
