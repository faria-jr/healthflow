"""Patient repository implementation."""

from datetime import date
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Patient
from application.interfaces.repositories import PatientRepository


class SQLAlchemyPatientRepository(PatientRepository):
    """SQLAlchemy implementation of patient repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, patient: Patient) -> Patient:
        """Create a new patient."""
        from database.models import Patient as PatientModel

        db_patient = PatientModel(
            user_id=patient.user_id,
            full_name=patient.full_name,
            cpf=patient.cpf,
            phone=patient.phone,
            email=patient.email,
            birth_date=patient.birth_date,
            gender=patient.gender,
            address=patient.address,
            emergency_contact=patient.emergency_contact,
            medical_history=patient.medical_history,
            allergies=patient.allergies,
        )
        self._session.add(db_patient)
        await self._session.flush()
        await self._session.refresh(db_patient)

        patient.id = db_patient.id
        return patient

    async def get_by_id(self, patient_id: int) -> Patient | None:
        """Get patient by ID."""
        from database.models import Patient as PatientModel

        result = await self._session.execute(
            select(PatientModel).where(PatientModel.id == patient_id)
        )
        db_patient = result.scalar_one_or_none()

        if db_patient is None:
            return None

        return self._to_entity(db_patient)

    async def get_by_user_id(self, user_id: UUID) -> Patient | None:
        """Get patient by user ID."""
        from database.models import Patient as PatientModel

        result = await self._session.execute(
            select(PatientModel).where(PatientModel.user_id == user_id)
        )
        db_patient = result.scalar_one_or_none()

        if db_patient is None:
            return None

        return self._to_entity(db_patient)

    async def get_by_cpf(self, cpf: str) -> Patient | None:
        """Get patient by CPF."""
        from database.models import Patient as PatientModel

        # Normalize CPF
        cpf_normalized = "".join(filter(str.isdigit, cpf))

        result = await self._session.execute(
            select(PatientModel).where(
                PatientModel.cpf == cpf_normalized
            )
        )
        db_patient = result.scalar_one_or_none()

        if db_patient is None:
            return None

        return self._to_entity(db_patient)

    async def get_by_email(self, email: str) -> Patient | None:
        """Get patient by email."""
        from database.models import Patient as PatientModel

        result = await self._session.execute(
            select(PatientModel).where(
                PatientModel.email == email.lower()
            )
        )
        db_patient = result.scalar_one_or_none()

        if db_patient is None:
            return None

        return self._to_entity(db_patient)

    async def update(self, patient: Patient) -> Patient:
        """Update patient."""
        from database.models import Patient as PatientModel

        result = await self._session.execute(
            select(PatientModel).where(PatientModel.id == patient.id)
        )
        db_patient = result.scalar_one()

        db_patient.full_name = patient.full_name
        db_patient.phone = patient.phone
        db_patient.address = patient.address
        db_patient.emergency_contact = patient.emergency_contact
        db_patient.medical_history = patient.medical_history
        db_patient.allergies = patient.allergies

        await self._session.flush()
        await self._session.refresh(db_patient)

        return patient

    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Patient]:
        """List patients with optional filters."""
        from database.models import Patient as PatientModel

        query = select(PatientModel)

        if filters:
            if "name" in filters:
                query = query.where(
                    PatientModel.full_name.ilike(f"%{filters['name']}%")
                )

        query = query.limit(limit).offset(offset)
        result = await self._session.execute(query)

        return [self._to_entity(p) for p in result.scalars().all()]

    def _to_entity(self, db_patient: Any) -> Patient:
        """Convert database model to domain entity."""
        return Patient(
            id=db_patient.id,
            user_id=db_patient.user_id,
            full_name=db_patient.full_name,
            cpf=db_patient.cpf,
            phone=db_patient.phone,
            email=db_patient.email,
            birth_date=db_patient.birth_date,
            gender=db_patient.gender,
            address=db_patient.address,
            emergency_contact=db_patient.emergency_contact,
            medical_history=db_patient.medical_history or {},
            allergies=db_patient.allergies or [],
        )
