"""Appointment model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .doctor import Doctor
    from .medical_record import MedicalRecord
    from .patient import Patient


class Appointment(Base, TimestampMixin):
    """Appointment entity."""

    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    patient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    doctor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="scheduled",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True, default=dict
    )

    # Relationships
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    medical_record: Mapped["MedicalRecord | None"] = relationship(
        back_populates="appointment",
        uselist=False,
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'confirmed', 'completed', 'cancelled', 'no_show')",
            name="ck_appointments_status",
        ),
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_appointments_duration_positive",
        ),
        Index("ix_appointments_patient_id", "patient_id"),
        Index("ix_appointments_doctor_id", "doctor_id"),
        Index("ix_appointments_scheduled_at", "scheduled_at"),
        Index("ix_appointments_status", "status"),
        Index("ix_appointments_patient_scheduled", "patient_id", "scheduled_at"),
        Index("ix_appointments_doctor_scheduled", "doctor_id", "scheduled_at"),
        Index(
            "ix_appointments_doctor_time_range",
            "doctor_id",
            "scheduled_at",
            "duration_minutes",
        ),
        Index(
            "ix_appointments_status_scheduled",
            "status",
            postgresql_where="status IN ('scheduled', 'confirmed')",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Appointment(id={self.id}, patient={self.patient_id}, "
            f"doctor={self.doctor_id}, at={self.scheduled_at})>"
        )
