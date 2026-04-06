"""Patient service."""

from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

from domain.entities import Patient
from domain.exceptions import (
    PatientAlreadyExistsError,
    PatientNotFoundError,
)
from application.interfaces.repositories import PatientRepository


@dataclass
class CreatePatientInput:
    """Input for creating a patient."""
    user_id: UUID
    full_name: str
    cpf: str
    email: str
    birth_date: date
    gender: str
    phone: str | None = None
    address: str | None = None


@dataclass
class UpdatePatientInput:
    """Input for updating a patient."""
    full_name: str | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: dict[str, Any] | None = None


class PatientService:
    """Patient service."""

    def __init__(self, repository: PatientRepository):
        self._repository = repository

    async def create_patient(self, input_data: CreatePatientInput) -> Patient:
        """Create a new patient.
        
        Args:
            input_data: Patient creation data
            
        Returns:
            Created patient
            
        Raises:
            PatientAlreadyExistsError: If CPF or email already exists
        """
        # Check if CPF already exists
        existing = await self._repository.get_by_cpf(input_data.cpf)
        if existing:
            raise PatientAlreadyExistsError(
                f"Patient with CPF {input_data.cpf} already exists"
            )

        # Check if email already exists
        existing = await self._repository.get_by_email(input_data.email)
        if existing:
            raise PatientAlreadyExistsError(
                f"Patient with email {input_data.email} already exists"
            )

        patient = Patient(
            user_id=input_data.user_id,
            full_name=input_data.full_name,
            cpf=input_data.cpf,
            email=input_data.email,
            birth_date=input_data.birth_date,
            gender=input_data.gender,
            phone=input_data.phone,
            address=input_data.address,
        )

        return await self._repository.create(patient)

    async def get_patient(self, patient_id: int) -> Patient:
        """Get patient by ID.
        
        Args:
            patient_id: Patient ID
            
        Returns:
            Patient
            
        Raises:
            PatientNotFoundError: If patient not found
        """
        patient = await self._repository.get_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient with ID {patient_id} not found")
        return patient

    async def get_patient_by_user(self, user_id: UUID) -> Patient:
        """Get patient by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Patient
            
        Raises:
            PatientNotFoundError: If patient not found
        """
        patient = await self._repository.get_by_user_id(user_id)
        if not patient:
            raise PatientNotFoundError(f"Patient for user {user_id} not found")
        return patient

    async def update_patient(
        self,
        patient_id: int,
        input_data: UpdatePatientInput,
    ) -> Patient:
        """Update patient.
        
        Args:
            patient_id: Patient ID
            input_data: Update data
            
        Returns:
            Updated patient
        """
        patient = await self.get_patient(patient_id)

        if input_data.full_name:
            patient.full_name = input_data.full_name
        if input_data.phone is not None:
            patient.phone = input_data.phone
        if input_data.address is not None:
            patient.address = input_data.address
        if input_data.emergency_contact is not None:
            patient.emergency_contact = input_data.emergency_contact

        return await self._repository.update(patient)

    async def add_medical_history(
        self,
        patient_id: int,
        data: dict[str, Any],
    ) -> Patient:
        """Add to patient medical history.
        
        Args:
            patient_id: Patient ID
            data: Medical history data to add
            
        Returns:
            Updated patient
        """
        patient = await self.get_patient(patient_id)
        patient.update_medical_history(data)
        return await self._repository.update(patient)

    async def add_allergy(self, patient_id: int, allergy: str) -> Patient:
        """Add allergy to patient.
        
        Args:
            patient_id: Patient ID
            allergy: Allergy to add
            
        Returns:
            Updated patient
        """
        patient = await self.get_patient(patient_id)
        patient.add_allergy(allergy)
        return await self._repository.update(patient)

    async def remove_allergy(self, patient_id: int, allergy: str) -> Patient:
        """Remove allergy from patient.
        
        Args:
            patient_id: Patient ID
            allergy: Allergy to remove
            
        Returns:
            Updated patient
        """
        patient = await self.get_patient(patient_id)
        patient.remove_allergy(allergy)
        return await self._repository.update(patient)

    async def list_patients(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Patient]:
        """List patients.
        
        Args:
            filters: Optional filters
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of patients
        """
        return await self._repository.list(filters, limit, offset)
