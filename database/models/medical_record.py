"""Medical Record model."""

from sqlalchemy import BigInteger, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .appointment import Appointment
    from .doctor import Doctor
    from .patient import Patient


class MedicalRecord(Base, TimestampMixin):
    """Medical Record entity."""

    __tablename__ = "medical_records"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
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
    doctor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
    )
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    prescription: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    attachments: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB, nullable=True, default=list
    )

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        back_populates="medical_record"
    )
    patient: Mapped["Patient"] = relationship(back_populates="medical_records")
    doctor: Mapped["Doctor"] = relationship(back_populates="medical_records")

    # Constraints
    __table_args__ = (
        Index("ix_medical_records_appointment_id", "appointment_id"),
        Index("ix_medical_records_patient_id", "patient_id"),
        Index("ix_medical_records_doctor_id", "doctor_id"),
        Index("ix_medical_records_created_at", "created_at"),
        Index(
            "ix_medical_records_patient_created",
            "patient_id",
            "created_at",
        ),
        Index(
            "ix_medical_records_doctor_created",
            "doctor_id",
            "created_at",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<MedicalRecord(id={self.id}, patient={self.patient_id}, "
            f"doctor={self.doctor_id})>"
        )
