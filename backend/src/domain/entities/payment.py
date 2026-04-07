"""Payment entity."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.exceptions import ValidationError


@dataclass
class Payment:
    """Payment aggregate root."""
    
    appointment_id: int
    patient_id: int
    amount: Decimal
    currency: str = "BRL"
    id: int | None = None
    status: str = "pending"  # pending, processing, completed, failed, refunded
    provider: str | None = None
    provider_payment_id: str | None = None
    paid_at: datetime | None = None
    refunded_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate payment data."""
        if self.amount <= 0:
            raise ValidationError("Payment amount must be positive")
        
        if self.currency not in ("BRL", "USD", "EUR"):
            raise ValidationError(f"Unsupported currency: {self.currency}")
        
        valid_statuses = {"pending", "processing", "completed", "failed", "refunded"}
        if self.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {self.status}")
    
    def mark_as_processing(self) -> None:
        """Mark payment as processing."""
        if self.status != "pending":
            raise ValidationError(f"Cannot process payment with status: {self.status}")
        self.status = "processing"
    
    def mark_as_completed(self) -> None:
        """Mark payment as completed."""
        from datetime import timezone
        if self.status not in ("pending", "processing"):
            raise ValidationError(f"Cannot complete payment with status: {self.status}")
        self.status = "completed"
        self.paid_at = datetime.now(timezone.utc)
    
    def mark_as_failed(self) -> None:
        """Mark payment as failed."""
        if self.status not in ("pending", "processing"):
            raise ValidationError(f"Cannot fail payment with status: {self.status}")
        self.status = "failed"
    
    def refund(self) -> None:
        """Refund payment."""
        from datetime import timezone
        if self.status != "completed":
            raise ValidationError(f"Cannot refund payment with status: {self.status}")
        self.status = "refunded"
        self.refunded_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status,
            "provider": self.provider,
            "provider_payment_id": self.provider_payment_id,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "refunded_at": self.refunded_at.isoformat() if self.refunded_at else None,
        }
