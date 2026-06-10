from app.models.aero_enums import NotificationChannel
from .aero_base_schema import TimestampSchema


class NotificationResponseSchema(TimestampSchema):
    user_id: int
    message: str
    channel: NotificationChannel
    status: str
