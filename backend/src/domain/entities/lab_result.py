"""Lab result entity."""

from dataclasses import dataclass
from datetime import datetime

from domain.exceptions import ValidationError


@dataclass
class LabResult:
    """Lab result aggregate root."""
    
    patient_id: int
    lab_name: str
    test_type: str
    id: int | None = None
    doctor_id: int | None = None
    appointment_id: int | None = None
    result_summary: str | None = None
    file_url: str | None = None
    file_name: str | None = None
    file_size: int | None = None
    status: str = "pending"  # pending, processing, completed, failed
    uploaded_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate lab result data."""
        if not self.lab_name or len(self.lab_name) > 200:
            raise ValidationError("Lab name must be between 1 and 200 characters")
        
        if not self.test_type or len(self.test_type) > 200:
            raise ValidationError("Test type must be between 1 and 200 characters")
        
        valid_statuses = {"pending", "processing", "completed", "failed"}
        if self.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {self.status}")
        
        if self.file_size and self.file_size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError("File size must be less than 10MB")
        
        if self.result_summary and len(self.result_summary) > 5000:
            raise ValidationError("Result summary must be less than 5000 characters")
    
    def mark_as_processing(self) -> None:
        """Mark as processing."""
        if self.status != "pending":
            raise ValidationError(f"Cannot process from status: {self.status}")
        self.status = "processing"
    
    def mark_as_completed(self) -> None:
        """Mark as completed."""
        if self.status not in ("pending", "processing"):
            raise ValidationError(f"Cannot complete from status: {self.status}")
        self.status = "completed"
    
    def mark_as_failed(self) -> None:
        """Mark as failed."""
        if self.status not in ("pending", "processing"):
            raise ValidationError(f"Cannot fail from status: {self.status}")
        self.status = "failed"
    
    def attach_file(self, url: str, name: str, size: int) -> None:
        """Attach file to result."""
        if size > 10 * 1024 * 1024:
            raise ValidationError("File size must be less than 10MB")
        self.file_url = url
        self.file_name = name
        self.file_size = size
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "lab_name": self.lab_name,
            "test_type": self.test_type,
            "result_summary": self.result_summary,
            "file_url": self.file_url,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "status": self.status,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }
