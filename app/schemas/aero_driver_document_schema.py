from datetime import date
from pydantic import BaseModel, Field

from app.models.aero_enums import DocumentType
from .aero_base_schema import TimestampSchema


class DriverDocumentCreateSchema(BaseModel):
    driver_id: int = Field(..., description="ID of the driver")
    document_type: DocumentType = Field(..., description="Type of the document")
    file_path: str = Field(..., description="File path of the document")
    expiry_date: date = Field(..., description="Expiry date of the document")


class DriverDocumentResponseSchema(TimestampSchema):
    driver_id: int = Field(..., description="ID of the driver")
    document_type: DocumentType = Field(..., description="Type of the document")
    file_path: str = Field(..., description="File path of the document")
    expiry_date: date = Field(..., description="Expiry date of the document")
    verified: bool = Field(..., description="Whether the document is verified")
