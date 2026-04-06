"""Patient model."""

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .appointment import Appointment
    from .medical_record import MedicalRecord


class Patient(Base, TimestampMixin):
    """Patient entity."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    cpf: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )
    medical_history: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True, default=dict
    )
    allergies: Mapped[list[str] | None] = mapped_column(
        JSONB, nullable=True, default=list
    )

    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    medical_records: Mapped[list["MedicalRecord"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("cpf", name="uq_patients_cpf"),
        UniqueConstraint("email", name="uq_patients_email"),
        Index("ix_patients_user_id", "user_id"),
        Index("ix_patients_cpf", "cpf"),
        Index("ix_patients_email", "email"),
        Index("ix_patients_full_name", "full_name"),
    )

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, name={self.full_name}, cpf={self.cpf})>"
