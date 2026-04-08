"""Lab result model."""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class LabResult(Base, TimestampMixin):
    """Lab result entity."""
    
    __tablename__ = "lab_results"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    doctor_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        nullable=True,
    )
    appointment_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("appointments.id", ondelete="SET NULL"),
        nullable=True,
    )
    lab_name: Mapped[str] = mapped_column(Text, nullable=False)
    test_type: Mapped[str] = mapped_column(Text, nullable=False)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="pending",  # pending, processing, completed, failed
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    
    __table_args__ = (
        {"comment": "Lab results and exam files"},
    )
    
    def __repr__(self) -> str:
        return f"<LabResult(id={self.id}, test_type={self.test_type}, status={self.status})>"
