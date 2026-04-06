"""Doctor service."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from domain.entities import Doctor
from domain.exceptions import (
    DoctorAlreadyExistsError,
    DoctorNotFoundError,
)
from application.interfaces.repositories import DoctorRepository


@dataclass
class CreateDoctorInput:
    """Input for creating a doctor."""
    user_id: UUID
    full_name: str
    crm: str
    specialty: str
    email: str
    phone: str | None = None
    bio: str | None = None
    consultation_fee: Decimal | None = None


@dataclass
class UpdateDoctorInput:
    """Input for updating a doctor."""
    full_name: str | None = None
    specialty: str | None = None
    phone: str | None = None
    bio: str | None = None
    consultation_fee: Decimal | None = None
    is_active: bool | None = None


class DoctorService:
    """Doctor service."""

    def __init__(self, repository: DoctorRepository):
        self._repository = repository

    async def create_doctor(self, input_data: CreateDoctorInput) -> Doctor:
        """Create a new doctor.
        
        Args:
            input_data: Doctor creation data
            
        Returns:
            Created doctor
            
        Raises:
            DoctorAlreadyExistsError: If CRM already exists
        """
        # Check if CRM already exists
        existing = await self._repository.get_by_crm(input_data.crm)
        if existing:
            raise DoctorAlreadyExistsError(
                f"Doctor with CRM {input_data.crm} already exists"
            )

        doctor = Doctor(
            user_id=input_data.user_id,
            full_name=input_data.full_name,
            crm=input_data.crm,
            specialty=input_data.specialty,
            email=input_data.email,
            phone=input_data.phone,
            bio=input_data.bio,
            consultation_fee=input_data.consultation_fee,
        )

        return await self._repository.create(doctor)

    async def get_doctor(self, doctor_id: int) -> Doctor:
        """Get doctor by ID.
        
        Args:
            doctor_id: Doctor ID
            
        Returns:
            Doctor
            
        Raises:
            DoctorNotFoundError: If doctor not found
        """
        doctor = await self._repository.get_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor with ID {doctor_id} not found")
        return doctor

    async def get_doctor_by_user(self, user_id: UUID) -> Doctor:
        """Get doctor by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Doctor
            
        Raises:
            DoctorNotFoundError: If doctor not found
        """
        doctor = await self._repository.get_by_user_id(user_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor for user {user_id} not found")
        return doctor

    async def update_doctor(
        self,
        doctor_id: int,
        input_data: UpdateDoctorInput,
    ) -> Doctor:
        """Update doctor.
        
        Args:
            doctor_id: Doctor ID
            input_data: Update data
            
        Returns:
            Updated doctor
        """
        doctor = await self.get_doctor(doctor_id)

        if input_data.full_name:
            doctor.full_name = input_data.full_name
        if input_data.specialty:
            doctor.specialty = input_data.specialty
        if input_data.phone is not None:
            doctor.phone = input_data.phone
        if input_data.bio is not None:
            doctor.bio = input_data.bio
        if input_data.consultation_fee is not None:
            doctor.update_fee(input_data.consultation_fee)
        if input_data.is_active is not None:
            if input_data.is_active:
                doctor.activate()
            else:
                doctor.deactivate()

        return await self._repository.update(doctor)

    async def deactivate_doctor(self, doctor_id: int) -> Doctor:
        """Deactivate doctor.
        
        Args:
            doctor_id: Doctor ID
            
        Returns:
            Updated doctor
        """
        doctor = await self.get_doctor(doctor_id)
        doctor.deactivate()
        return await self._repository.update(doctor)

    async def activate_doctor(self, doctor_id: int) -> Doctor:
        """Activate doctor.
        
        Args:
            doctor_id: Doctor ID
            
        Returns:
            Updated doctor
        """
        doctor = await self.get_doctor(doctor_id)
        doctor.activate()
        return await self._repository.update(doctor)

    async def list_doctors(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors.
        
        Args:
            filters: Optional filters (specialty, name, is_active)
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of doctors
        """
        return await self._repository.list(filters, limit, offset)

    async def list_doctors_by_specialty(
        self,
        specialty: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors by specialty.
        
        Args:
            specialty: Specialty to filter by
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of doctors
        """
        return await self._repository.list_by_specialty(specialty, limit, offset)

    async def search_doctors(
        self,
        query: str,
        specialty: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """Search doctors by name or specialty.
        
        Args:
            query: Search query for name
            specialty: Optional specialty filter
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of doctors
        """
        filters: dict[str, Any] = {"name": query}
        if specialty:
            filters["specialty"] = specialty
        return await self._repository.list(filters, limit, offset)
