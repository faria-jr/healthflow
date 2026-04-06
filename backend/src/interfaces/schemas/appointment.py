"""Appointment schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AppointmentBase(BaseModel):
    """Base appointment schema."""

    model_config = ConfigDict(from_attributes=True)

    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    duration_minutes: int = Field(30, ge=15, le=480)
    notes: str | None = Field(None, max_length=1000)


class AppointmentCreate(AppointmentBase):
    """Appointment creation schema."""

    @field_validator("scheduled_at")
    @classmethod
    def validate_future_date(cls, v: datetime) -> datetime:
        """Validate that scheduled_at is in the future."""
        from datetime import timezone

        if v < datetime.now(timezone.utc):
            raise ValueError("Scheduled time must be in the future")
        return v


class AppointmentUpdateStatus(BaseModel):
    """Appointment status update schema."""

    status: str = Field(
        ...,
        pattern="^(scheduled|confirmed|completed|cancelled|no_show)$",
    )
    reason: str | None = Field(None, max_length=500)


class AppointmentResponse(BaseModel):
    """Appointment response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    end_time: datetime
    duration_minutes: int
    status: str
    notes: str | None
    cancellation_reason: str | None
    metadata: dict[str, Any]
    created_at: str
    updated_at: str


class AppointmentListResponse(BaseModel):
    """Appointment list response."""

    appointments: list[AppointmentResponse]
    total: int


class AppointmentFilterRequest(BaseModel):
    """Appointment filter request."""

    status: str | None = Field(
        None,
        pattern="^(scheduled|confirmed|completed|cancelled|no_show)$",
    )
    from_date: datetime | None = None
    to_date: datetime | None = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)


class AddNotesRequest(BaseModel):
    """Add notes request."""

    notes: str = Field(..., max_length=1000)
