"""Payment model."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Payment(Base, TimestampMixin):
    """Payment entity."""
    
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    appointment_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    patient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(Text, nullable=False, default="BRL")
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="pending",  # pending, processing, completed, failed, refunded
    )
    provider: Mapped[str] = mapped_column(Text, nullable=False)  # stripe, pagarme
    provider_payment_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"comment": "Payments for appointments"},
    )
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"
