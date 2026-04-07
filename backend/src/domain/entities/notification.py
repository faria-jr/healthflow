"""Notification entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from domain.exceptions import ValidationError


@dataclass
class Notification:
    """Notification aggregate root."""
    
    user_id: UUID
    type: str  # email, sms, push
    title: str
    body: str
    id: int | None = None
    data: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending, sent, failed, read
    sent_at: datetime | None = None
    read_at: datetime | None = None
    created_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate notification data."""
        valid_types = {"email", "sms", "push"}
        if self.type not in valid_types:
            raise ValidationError(f"Invalid notification type: {self.type}")
        
        valid_statuses = {"pending", "sent", "failed", "read"}
        if self.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {self.status}")
        
        if not self.title or len(self.title) > 200:
            raise ValidationError("Title must be between 1 and 200 characters")
        
        if not self.body or len(self.body) > 2000:
            raise ValidationError("Body must be between 1 and 2000 characters")
    
    def mark_as_sent(self) -> None:
        """Mark notification as sent."""
        from datetime import timezone
        if self.status != "pending":
            raise ValidationError(f"Cannot mark as sent from status: {self.status}")
        self.status = "sent"
        self.sent_at = datetime.now(timezone.utc)
    
    def mark_as_failed(self) -> None:
        """Mark notification as failed."""
        if self.status != "pending":
            raise ValidationError(f"Cannot mark as failed from status: {self.status}")
        self.status = "failed"
    
    def mark_as_read(self) -> None:
        """Mark notification as read."""
        from datetime import timezone
        if self.status != "sent":
            raise ValidationError(f"Cannot mark as read from status: {self.status}")
        self.status = "read"
        self.read_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "type": self.type,
            "title": self.title,
            "body": self.body,
            "data": self.data,
            "status": self.status,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
        }


@dataclass
class NotificationPreference:
    """User notification preferences."""
    
    user_id: UUID
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    reminder_hours: int = 24
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate preferences."""
        if not 1 <= self.reminder_hours <= 72:
            raise ValidationError("Reminder hours must be between 1 and 72")
    
    def should_notify(self, channel: str) -> bool:
        """Check if user should be notified via channel."""
        channels = {
            "email": self.email_enabled,
            "sms": self.sms_enabled,
            "push": self.push_enabled,
        }
        return channels.get(channel, False)
    
    def update_preferences(
        self,
        email: bool | None = None,
        sms: bool | None = None,
        push: bool | None = None,
        reminder_hours: int | None = None,
    ) -> None:
        """Update notification preferences."""
        if email is not None:
            self.email_enabled = email
        if sms is not None:
            self.sms_enabled = sms
        if push is not None:
            self.push_enabled = push
        if reminder_hours is not None:
            if not 1 <= reminder_hours <= 72:
                raise ValidationError("Reminder hours must be between 1 and 72")
            self.reminder_hours = reminder_hours
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "email_enabled": self.email_enabled,
            "sms_enabled": self.sms_enabled,
            "push_enabled": self.push_enabled,
            "reminder_hours": self.reminder_hours,
        }
