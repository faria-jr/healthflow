"""Appointment service."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from domain.entities import Appointment
from domain.exceptions import (
    AppointmentConflictError,
    AppointmentNotFoundError,
    AppointmentStatusError,
)
from application.interfaces.repositories import (
    AppointmentRepository,
    PatientRepository,
    DoctorRepository,
)


@dataclass
class ScheduleAppointmentInput:
    """Input for scheduling an appointment."""
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    duration_minutes: int = 30
    notes: str | None = None


@dataclass
class UpdateAppointmentStatusInput:
    """Input for updating appointment status."""
    status: str
    reason: str | None = None


class AppointmentService:
    """Appointment service."""

    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        patient_repo: PatientRepository,
        doctor_repo: DoctorRepository,
    ):
        self._appointment_repo = appointment_repo
        self._patient_repo = patient_repo
        self._doctor_repo = doctor_repo

    async def schedule_appointment(
        self,
        input_data: ScheduleAppointmentInput,
    ) -> Appointment:
        """Schedule a new appointment.
        
        Args:
            input_data: Appointment scheduling data
            
        Returns:
            Created appointment
            
        Raises:
            AppointmentConflictError: If there's a scheduling conflict
        """
        # Verify patient exists
        patient = await self._patient_repo.get_by_id(input_data.patient_id)
        if not patient:
            raise AppointmentNotFoundError(
                f"Patient {input_data.patient_id} not found"
            )

        # Verify doctor exists
        doctor = await self._doctor_repo.get_by_id(input_data.doctor_id)
        if not doctor:
            raise AppointmentNotFoundError(
                f"Doctor {input_data.doctor_id} not found"
            )

        # Check for conflicts
        conflicts = await self._appointment_repo.check_conflicts(
            doctor_id=input_data.doctor_id,
            scheduled_at=input_data.scheduled_at,
            duration_minutes=input_data.duration_minutes,
        )

        if conflicts:
            conflict_times = [
                f"{c.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
                for c in conflicts
            ]
            raise AppointmentConflictError(
                f"Doctor has conflicting appointments at: {', '.join(conflict_times)}"
            )

        appointment = Appointment(
            patient_id=input_data.patient_id,
            doctor_id=input_data.doctor_id,
            scheduled_at=input_data.scheduled_at,
            duration_minutes=input_data.duration_minutes,
            notes=input_data.notes,
        )

        return await self._appointment_repo.create(appointment)

    async def get_appointment(self, appointment_id: int) -> Appointment:
        """Get appointment by ID.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Appointment
            
        Raises:
            AppointmentNotFoundError: If appointment not found
        """
        appointment = await self._appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise AppointmentNotFoundError(
                f"Appointment with ID {appointment_id} not found"
            )
        return appointment

    async def update_status(
        self,
        appointment_id: int,
        input_data: UpdateAppointmentStatusInput,
    ) -> Appointment:
        """Update appointment status.
        
        Args:
            appointment_id: Appointment ID
            input_data: Status update data
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.transition_to(input_data.status, input_data.reason)
        return await self._appointment_repo.update(appointment)

    async def confirm_appointment(self, appointment_id: int) -> Appointment:
        """Confirm appointment.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.confirm()
        return await self._appointment_repo.update(appointment)

    async def complete_appointment(self, appointment_id: int) -> Appointment:
        """Complete appointment.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.complete()
        return await self._appointment_repo.update(appointment)

    async def cancel_appointment(
        self,
        appointment_id: int,
        reason: str | None = None,
    ) -> Appointment:
        """Cancel appointment.
        
        Args:
            appointment_id: Appointment ID
            reason: Cancellation reason
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.cancel(reason)
        return await self._appointment_repo.update(appointment)

    async def mark_no_show(self, appointment_id: int) -> Appointment:
        """Mark appointment as no-show.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.mark_no_show()
        return await self._appointment_repo.update(appointment)

    async def add_notes(
        self,
        appointment_id: int,
        notes: str,
    ) -> Appointment:
        """Add notes to appointment.
        
        Args:
            appointment_id: Appointment ID
            notes: Notes to add
            
        Returns:
            Updated appointment
        """
        appointment = await self.get_appointment(appointment_id)
        appointment.add_notes(notes)
        return await self._appointment_repo.update(appointment)

    async def list_patient_appointments(
        self,
        patient_id: int,
        status: str | None = None,
        from_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        """List appointments for a patient.
        
        Args:
            patient_id: Patient ID
            status: Optional status filter
            from_date: Optional from date filter
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of appointments
        """
        return await self._appointment_repo.list_by_patient(
            patient_id, status, from_date, limit, offset
        )

    async def list_doctor_appointments(
        self,
        doctor_id: int,
        status: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        """List appointments for a doctor.
        
        Args:
            doctor_id: Doctor ID
            status: Optional status filter
            from_date: Optional from date filter
            to_date: Optional to date filter
            limit: Maximum number of results
            offset: Offset for pagination