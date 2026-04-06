"""Medical Record entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from domain.exceptions import ValidationError


@dataclass
class MedicalRecord:
    """Medical Record aggregate root."""
    
    appointment_id: int
    patient_id: int
    doctor_id: int
    id: int | None = None
    diagnosis: str | None = None
    symptoms: str | None = None
    prescription: str | None = None
    notes: str | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate medical record data."""
        # At least one clinical field should be present
        clinical_fields = [
            self.diagnosis,
            self.symptoms,
            self.prescription,
            self.notes,
        ]
        if not any(clinical_fields) and not self.attachments:
            raise ValidationError(
                "Medical record must have at least one clinical field or attachment"
            )
    
    def update_diagnosis(self, diagnosis: str) -> None:
        """Update diagnosis."""
        self.diagnosis = diagnosis
    
    def update_symptoms(self, symptoms: str) -> None:
        """Update symptoms."""
        self.symptoms = symptoms
    
    def update_prescription(self, prescription: str) -> None:
        """Update prescription."""
        self.prescription = prescription
    
    def update_notes(self, notes: str) -> None:
        """Update notes."""
        self.notes = notes
    
    def add_attachment(self, attachment: dict[str, Any]) -> None:
        """Add attachment.
        
        Args:
            attachment: Dict with keys: name, url, type, size
        """
        required_keys = {"name", "url", "type"}
        if not required_keys.issubset(attachment.keys()):
            raise ValidationError(
                f"Attachment must have: {required_keys}"
            )
        
        self.attachments.append(attachment)
    
    def remove_attachment(self, attachment_name: str) -> bool:
        """Remove attachment by name.
        
        Args:
            attachment_name: Name of attachment to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, att in enumerate(self.attachments):
            if att.get("name") == attachment_name:
                self.attachments.pop(i)
                return True
        return False
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "diagnosis": self.diagnosis,
            "symptoms": self.symptoms,
            "prescription": self.prescription,
            "notes": self.notes,
            "attachments": self.attachments,
        }
