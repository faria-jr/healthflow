"""Appointment repository implementation."""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities import Appointment
from application.interfaces.repositories import AppointmentRepository


class SQLAlchemyAppointmentRepository(AppointmentRepository):
    """SQLAlchemy implementation of appointment repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, appointment: Appointment) -> Appointment:
        """Create a new appointment."""
        from database.models import Appointment as AppointmentModel

        db_appointment = AppointmentModel(
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            scheduled_at=appointment.scheduled_at,
            duration_minutes=appointment.duration_minutes,
            status=appointment.status,
            notes=appointment.notes,
            metadata=appointment.metadata,
        )
        self._session.add(db_appointment)
        await self._session.flush()
        await self._session.refresh(db_appointment)

        appointment.id = db_appointment.id
        appointment.created_at = db_appointment.created_at
        appointment.updated_at = db_appointment.updated_at
        return appointment

    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        """Get appointment by ID."""
        from database.models import Appointment as AppointmentModel

        result = await self._session.execute(
            select(AppointmentModel).where(
                AppointmentModel.id == appointment_id
            )
        )
        db_appointment = result.scalar_one_or_none()

        if db_appointment is None:
            return None

        return self._to_entity(db_appointment)

    async def update(self, appointment: Appointment) -> Appointment:
        """Update appointment."""
        from database.models import Appointment as AppointmentModel

        result = await self._session.execute(
            select(AppointmentModel).where(
                AppointmentModel.id == appointment.id
            )
        )
        db_appointment = result.scalar_one()

        db_appointment.status = appointment.status
        db_appointment.notes = appointment.notes
        db_appointment.cancellation_reason = appointment.cancellation_reason
        db_appointment.metadata = appointment.metadata

        await self._session.flush()
        await self._session.refresh(db_appointment)

        appointment.updated_at = db_appointment.updated_at
        return appointment

    async def list_by_patient(
        self,
        patient_id: int,
        status: str | None = None,
        from_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        """List appointments by patient."""
        from database.models import Appointment as AppointmentModel

        query = select(AppointmentModel).where(
            AppointmentModel.patient_id == patient_id
        )

        if status:
            query = query.where(AppointmentModel.status == status)

        if from_date:
            query = query.where(AppointmentModel.scheduled_at >= from_date)

        # Add eager loading for patient and doctor to avoid N+1
        query = query.options(
            selectinload(AppointmentModel.patient),
            selectinload(AppointmentModel.doctor),
        )

        query = (
            query.order_by(AppointmentModel.scheduled_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(query)
        return [self._to_entity(a) for a in result.scalars().all()]

    async def list_by_doctor(
        self,
        doctor_id: int,
        status: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        """List appointments by doctor."""
        from database.models import Appointment as AppointmentModel

        query = select(AppointmentModel).where(
            AppointmentModel.doctor_id == doctor_id
        )

        if status:
            query = query.where(AppointmentModel.status == status)

        if from_date:
            query = query.where(AppointmentModel.scheduled_at >= from_date)

        if to_date:
            query = query.where(AppointmentModel.scheduled_at <= to_date)

        # Add eager loading for patient and doctor to avoid N+1
        query = query.options(
            selectinload(AppointmentModel.patient),
            selectinload(AppointmentModel.doctor),
        )

        query = (
            query.order_by(AppointmentModel.scheduled_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(query)
        return [self._to_entity(a) for a in result.scalars().all()]

    async def check_conflicts(
        self,
        doctor_id: int,
        scheduled_at: datetime,
        duration_minutes: int,
        exclude_appointment_id: int | None = None,
    ) -> list[Appointment]:
        """Check for scheduling conflicts."""
        from database.models import Appointment as AppointmentModel

        end_time = scheduled_at + timedelta(minutes=duration_minutes)

        # Check for overlapping appointments
        query = select(AppointmentModel).where(
            and_(
                AppointmentModel.doctor_id == doctor_id,
                AppointmentModel.status.in_(["scheduled", "confirmed"]),
                or_(
                    # New appointment starts during existing
                    and_(
                        AppointmentModel.scheduled_at <= scheduled_at,
                        AppointmentModel.scheduled_at
                        + (AppointmentModel.duration_minutes * timedelta(minutes=1))
                        > scheduled_at,
                    ),
                    # New appointment ends during existing
                    and_(
                        AppointmentModel.scheduled_at < end_time,
                        AppointmentModel.scheduled_at
                        + (AppointmentModel.duration_minutes * timedelta(minutes=1))
                        >= end_time,
                    ),
                    # New appointment completely contains existing
                    and_(
                        AppointmentModel.scheduled_at >= scheduled_at,
                        AppointmentModel.scheduled_at
                        + (AppointmentModel.duration_minutes * timedelta(minutes=1))
                        <= end_time,
                    ),
                ),
            )
        )

        if exclude_appointment_id:
            query = query.where(
                AppointmentModel.id != exclude_appointment_id
            )

        result = await self._session.execute(query)
        return [self._to_entity(a) for a in result.scalars().all()]

    def _to_entity(self, db_appointment: Any) -> Appointment:
        """Convert database model to domain entity."""
        return Appointment(
            id=db_appointment.id,
            patient_id=db_appointment.patient_id,
            doctor_id=db_appointment.doctor_id,
            scheduled_at=db_appointment.scheduled_at,
            duration_minutes=db_appointment.duration_minutes,
            status=db_appointment.status,
            notes=db_appointment.notes,
            cancellation_reason=db_appointment.cancellation_reason,
            metadata=db_appointment.metadata or {},
            created_at=db_appointment.created_at,
            updated_at=db_appointment.updated_at,
        )
