"""Doctor model."""

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, ForeignKey, Index, Numeric, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .appointment import Appointment
    from .medical_record import MedicalRecord


class Doctor(Base, TimestampMixin):
    """Doctor entity."""

    __tablename__ = "doctors"

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
    crm: Mapped[str] = mapped_column(Text, nullable=False)
    specialty: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    consultation_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
    )
    medical_records: Mapped[list["MedicalRecord"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("crm", name="uq_doctors_crm"),
        UniqueConstraint("email", name="uq_doctors_email"),
        Index("ix_doctors_user_id", "user_id"),
        Index("ix_doctors_crm", "crm"),
        Index("ix_doctors_specialty", "specialty"),
        Index("ix_doctors_is_active", "is_active"),
        Index("ix_doctors_specialty_active", "specialty", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name={self.full_name}, crm={self.crm})>"
