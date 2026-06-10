from sqlalchemy import ForeignKey, String, Enum, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.aero_base_model import Base, TimestampMixin, UUIDMixin
from app.models.aero_enums import DocumentType


class DriverDocument(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "driver_documents"

    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), nullable=False)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255))
    expiry_date: Mapped[Date] = mapped_column(Date, nullable=True)
    verified: Mapped[bool] = mapped_column(default=False)

    driver = relationship("Driver", back_populates="documents")
