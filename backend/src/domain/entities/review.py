"""Review entity."""

from dataclasses import dataclass
from datetime import datetime

from domain.exceptions import ValidationError


@dataclass
class Review:
    """Review aggregate root."""
    
    doctor_id: int
    patient_id: int
    appointment_id: int
    rating: int
    id: int | None = None
    comment: str | None = None
    is_anonymous: bool = False
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate review data."""
        if not 1 <= self.rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")
        
        valid_statuses = {"pending", "approved", "rejected"}
        if self.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {self.status}")
        
        if self.comment and len(self.comment) > 2000:
            raise ValidationError("Comment must be less than 2000 characters")
    
    def approve(self) -> None:
        """Approve review."""
        if self.status != "pending":
            raise ValidationError(f"Cannot approve review with status: {self.status}")
        self.status = "approved"
    
    def reject(self) -> None:
        """Reject review."""
        if self.status != "pending":
            raise ValidationError(f"Cannot reject review with status: {self.status}")
        self.status = "rejected"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "appointment_id": self.appointment_id,
            "rating": self.rating,
            "comment": self.comment,
            "is_anonymous": self.is_anonymous,
            "status": self.status,
        }
