"""Appointment entity."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from domain.exceptions import (
    AppointmentStatusError,
    InvalidAppointmentTimeError,
)


APPOINTMENT_STATUSES = {
    "scheduled",
    "confirmed",
    "completed",
    "cancelled",
    "no_show",
}

VALID_TRANSITIONS = {
    "scheduled": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled", "no_show"},
    "completed": set(),  # Terminal state
    "cancelled": set(),  # Terminal state
    "no_show": set(),    # Terminal state
}


@dataclass
class Appointment:
    """Appointment aggregate root."""
    
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    id: int | None = None
    duration_minutes: int = 30
    status: str = "scheduled"
    notes: str | None = None
    cancellation_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate appointment data."""
        if self.duration_minutes <= 0:
            raise InvalidAppointmentTimeError("Duration must be positive")
        
        if self.status not in APPOINTMENT_STATUSES:
            raise InvalidAppointmentTimeError(
                f"Invalid status: {self.status}. Must be one of: {APPOINTMENT_STATUSES}"
            )
        
        # Check if scheduled_at is in the future (for new appointments)
        if self.id is None and self.created_at is None:
            from datetime import timezone
            now = datetime.now(timezone.utc)
            if self.scheduled_at < now:
                raise InvalidAppointmentTimeError(
                    "Cannot schedule appointment in the past"
                )
    
    @property
    def end_time(self) -> datetime:
        """Calculate appointment end time."""
        return self.scheduled_at + timedelta(minutes=self.duration_minutes)
    
    def overlaps_with(self, other: "Appointment") -> bool:
        """Check if this appointment overlaps with another.
        
        Args:
            other: Another appointment to check against
            
        Returns:
            True if appointments overlap
        """
        # Same doctor and overlapping times
        if self.doctor_id != other.doctor_id:
            return False
        
        return (
            self.scheduled_at < other.end_time
            and other.scheduled_at < self.end_time
        )
    
    def can_transition_to(self, new_status: str) -> bool:
        """Check if status transition is valid.
        
        Args:
            new_status: Target status
            
        Returns:
            True if transition is valid
        """
        if new_status not in APPOINTMENT_STATUSES:
            return False
        
        valid_next = VALID_TRANSITIONS.get(self.status, set())
        return new_status in valid_next
    
    def transition_to(self, new_status: str, reason: str | None = None) -> None:
        """Transition to new status.
        
        Args:
            new_status: Target status
            reason: Optional reason for transition (e.g., cancellation)
            
        Raises:
            AppointmentStatusError: If transition is invalid
        """
        if not self.can_transition_to(new_status):
            raise AppointmentStatusError(
                f"Cannot transition from {self.status} to {new_status}"
            )
        
        self.status = new_status
        
        if new_status == "cancelled" and reason:
            self.cancellation_reason = reason
    
    def confirm(self) -> None:
        """Confirm appointment."""
        self.transition_to("confirmed")
    
    def complete(self) -> None:
        """Complete appointment."""
        self.transition_to("completed")
    
    def cancel(self, reason: str | None = None) -> None:
        """Cancel appointment."""
        self.transition_to("cancelled", reason)
    
    def mark_no_show(self) -> None:
        """Mark as no-show."""
        self.transition_to("no_show")
    
    def add_notes(self, notes: str) -> None:
        """Add notes to appointment."""
        self.notes = notes
    
    def update_metadata(self, data: dict[str, Any]) -> None:
        """Update metadata."""
        self.metadata.update(data)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "scheduled_at": self.scheduled_at.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "status": self.status,
            "notes": self.notes,
            "cancellation_reason": self.cancellation_reason,
            "metadata": self.metadata,
        }
