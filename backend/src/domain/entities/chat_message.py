"""Chat message entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from domain.exceptions import ValidationError


@dataclass
class ChatMessage:
    """Chat message aggregate root."""
    
    appointment_id: int
    sender_id: UUID
    sender_type: str  # patient, doctor
    content: str
    id: int | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)
    sent_at: datetime | None = None
    read_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate message data."""
        valid_sender_types = {"patient", "doctor"}
        if self.sender_type not in valid_sender_types:
            raise ValidationError(f"Invalid sender type: {self.sender_type}")
        
        if not self.content or len(self.content) > 4000:
            raise ValidationError("Content must be between 1 and 4000 characters")
        
        # Validate attachments
        for att in self.attachments:
            if "url" not in att or "name" not in att:
                raise ValidationError("Attachment must have url and name")
    
    def mark_as_read(self) -> None:
        """Mark message as read."""
        from datetime import timezone
        if self.read_at is None:
            self.read_at = datetime.now(timezone.utc)
    
    def add_attachment(self, url: str, name: str, type: str, size: int | None = None) -> None:
        """Add attachment to message."""
        self.attachments.append({
            "url": url,
            "name": name,
            "type": type,
            "size": size,
        })
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "sender_id": str(self.sender_id),
            "sender_type": self.sender_type,
            "content": self.content,
            "attachments": self.attachments,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
        }
