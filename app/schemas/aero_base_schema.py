from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        orm_mode=True
    )


class TimestampSchema(ORMBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
