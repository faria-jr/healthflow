"""Review model."""

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Review(Base, TimestampMixin):
    """Review entity."""
    
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
    )
    patient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    appointment_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="pending",  # pending, approved, rejected
    )
    
    __table_args__ = (
        {"comment": "Doctor reviews by patients"},
    )
    
    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, status={self.status})>"
