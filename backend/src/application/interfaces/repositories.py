"""Repository interfaces."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import UUID

from domain.entities import Appointment, Doctor, MedicalRecord, Patient


class PatientRepository(ABC):
    """Patient repository interface."""

    @abstractmethod
    async def create(self, patient: Patient) -> Patient:
        """Create a new patient."""
        pass

    @abstractmethod
    async def get_by_id(self, patient_id: int) -> Patient | None:
        """Get patient by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Patient | None:
        """Get patient by user ID."""
        pass

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> Patient | None:
        """Get patient by CPF."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Patient | None:
        """Get patient by email."""
        pass

    @abstractmethod
    async def update(self, patient: Patient) -> Patient:
        """Update patient."""
        pass

    @abstractmethod
    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Patient]:
        """List patients with optional filters."""
        pass


class DoctorRepository(ABC):
    """Doctor repository interface."""

    @abstractmethod
    async def create(self, doctor: Doctor) -> Doctor:
        """Create a new doctor."""
        pass

    @abstractmethod
    async def get_by_id(self, doctor_id: int) -> Doctor | None:
        """Get doctor by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Doctor | None:
        """Get doctor by user ID."""
        pass

    @abstractmethod
    async def get_by_crm(self, crm: str) -> Doctor | None:
        """Get doctor by CRM."""
        pass

    @abstractmethod
    async def update(self, doctor: Doctor) -> Doctor:
        """Update doctor."""
        pass

    @abstractmethod
    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors with optional filters."""
        pass

    @abstractmethod
    async def list_by_specialty(
        self,
        specialty: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors by specialty."""
        pass


class AppointmentRepository(ABC):
    """Appointment repository interface."""

    @abstractmethod
    async def create(self, appointment: Appointment) -> Appointment:
        """Create a new appointment."""
        pass

    @abstractmethod
    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        """Get appointment by ID."""
        pass

    @abstractmethod
    async def update(self, appointment: Appointment) -> Appointment:
        """Update appointment."""
        pass

    @abstractmethod
    async def list_by_patient(
        self,
        patient_id: int,
        status: str | None = None,
        from_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        """List appointments by patient."""
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def check_conflicts(
        self,
        doctor_id: int,
        scheduled_at: datetime,
        duration_minutes: int,
        exclude_appointment_id: int | None = None,
    ) -> list[Appointment]:
        """Check for scheduling conflicts."""
        pass


class MedicalRecordRepository(ABC):
    """Medical record repository interface."""

    @abstractmethod
    async def create(self, record: MedicalRecord) -> MedicalRecord:
        """Create a new medical record."""
        pass

    @abstractmethod
    async def get_by_id(self, record_id: int) -> MedicalRecord | None:
        """Get medical record by ID."""
        pass

    @abstractmethod
    async def get_by_appointment_id(
        self, appointment_id: int
    ) -> MedicalRecord | None:
        """Get medical record by appointment ID."""
        pass

    @abstractmethod
    async def update(self, record: MedicalRecord) -> MedicalRecord:
        """Update medical record."""
        pass

    @abstractmethod
    async def list_by_patient(
        self,
        patient_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records by patient."""
        pass

    @abstractmethod
    async def list_by_doctor(
        self,
        doctor_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records by doctor."""
        pass


class PaymentRepository(ABC):
    """Payment repository interface."""

    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: int) -> Payment | None:
        """Get payment by ID."""
        pass

    @abstractmethod
    async def get_by_appointment_id(self, appointment_id: int) -> Payment | None:
        """Get payment by appointment ID."""
        pass

    @abstractmethod
    async def update(self, payment: Payment) -> Payment:
        """Update payment."""
        pass
