"""Medical record service."""

from dataclasses import dataclass
from typing import Any

from domain.entities import MedicalRecord
from domain.exceptions import (
    AppointmentNotFoundError,
    MedicalRecordAlreadyExistsError,
    MedicalRecordNotFoundError,
)
from application.interfaces.repositories import (
    MedicalRecordRepository,
    AppointmentRepository,
)


@dataclass
class CreateMedicalRecordInput:
    """Input for creating a medical record."""
    appointment_id: int
    diagnosis: str | None = None
    symptoms: str | None = None
    prescription: str | None = None
    notes: str | None = None


@dataclass
class UpdateMedicalRecordInput:
    """Input for updating a medical record."""
    diagnosis: str | None = None
    symptoms: str | None = None
    prescription: str | None = None
    notes: str | None = None


class MedicalRecordService:
    """Medical record service."""

    def __init__(
        self,
        record_repo: MedicalRecordRepository,
        appointment_repo: AppointmentRepository,
    ):
        self._record_repo = record_repo
        self._appointment_repo = appointment_repo

    async def create_medical_record(
        self,
        input_data: CreateMedicalRecordInput,
    ) -> MedicalRecord:
        """Create a medical record for an appointment.
        
        Args:
            input_data: Medical record creation data
            
        Returns:
            Created medical record
            
        Raises:
            AppointmentNotFoundError: If appointment not found
            MedicalRecordAlreadyExistsError: If record already exists
        """
        # Verify appointment exists
        appointment = await self._appointment_repo.get_by_id(
            input_data.appointment_id
        )
        if not appointment:
            raise AppointmentNotFoundError(
                f"Appointment {input_data.appointment_id} not found"
            )

        # Check if record already exists
        existing = await self._record_repo.get_by_appointment_id(
            input_data.appointment_id
        )
        if existing:
            raise MedicalRecordAlreadyExistsError(
                f"Medical record already exists for appointment {input_data.appointment_id}"
            )

        record = MedicalRecord(
            appointment_id=input_data.appointment_id,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            diagnosis=input_data.diagnosis,
            symptoms=input_data.symptoms,
            prescription=input_data.prescription,
            notes=input_data.notes,
        )

        return await self._record_repo.create(record)

    async def get_medical_record(self, record_id: int) -> MedicalRecord:
        """Get medical record by ID.
        
        Args:
            record_id: Medical record ID
            
        Returns:
            Medical record
            
        Raises:
            MedicalRecordNotFoundError: If record not found
        """
        record = await self._record_repo.get_by_id(record_id)
        if not record:
            raise MedicalRecordNotFoundError(
                f"Medical record with ID {record_id} not found"
            )
        return record

    async def get_medical_record_by_appointment(
        self,
        appointment_id: int,
    ) -> MedicalRecord:
        """Get medical record by appointment ID.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Medical record
            
        Raises:
            MedicalRecordNotFoundError: If record not found
        """
        record = await self._record_repo.get_by_appointment_id(appointment_id)
        if not record:
            raise MedicalRecordNotFoundError(
                f"Medical record for appointment {appointment_id} not found"
            )
        return record

    async def update_medical_record(
        self,
        record_id: int,
        input_data: UpdateMedicalRecordInput,
    ) -> MedicalRecord:
        """Update medical record.
        
        Args:
            record_id: Medical record ID
            input_data: Update data
            
        Returns:
            Updated medical record
        """
        record = await self.get_medical_record(record_id)

        if input_data.diagnosis is not None:
            record.update_diagnosis(input_data.diagnosis)
        if input_data.symptoms is not None:
            record.update_symptoms(input_data.symptoms)
        if input_data.prescription is not None:
            record.update_prescription(input_data.prescription)
        if input_data.notes is not None:
            record.update_notes(input_data.notes)

        return await self._record_repo.update(record)

    async def add_attachment(
        self,
        record_id: int,
        attachment: dict[str, Any],
    ) -> MedicalRecord:
        """Add attachment to medical record.
        
        Args:
            record_id: Medical record ID
            attachment: Attachment data (name, url, type, size)
            
        Returns:
            Updated medical record
        """
        record = await self.get_medical_record(record_id)
        record.add_attachment(attachment)
        return await self._record_repo.update(record)

    async def remove_attachment(
        self,
        record_id: int,
        attachment_name: str,
    ) -> MedicalRecord:
        """Remove attachment from medical record.
        
        Args:
            record_id: Medical record ID
            attachment_name: Name of attachment to remove
            
        Returns:
            Updated medical record
        """
        record = await self.get_medical_record(record_id)
        record.remove_attachment(attachment_name)
        return await self._record_repo.update(record)

    async def list_patient_records(
        self,
        patient_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records for a patient.
        
        Args:
            patient_id: Patient ID
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of medical records
        """
        return await self._record_repo.list_by_patient(
            patient_id, limit, offset
        )

    async def list_doctor_records(
        self,
        doctor_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records for a doctor.
        
        Args:
            doctor_id: Doctor ID
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of medical records
        """
        return await self._record_repo.list_by_doctor(
            doctor_id, limit, offset
        )
