"""Doctor repository implementation."""

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Doctor
from application.interfaces.repositories import DoctorRepository


class SQLAlchemyDoctorRepository(DoctorRepository):
    """SQLAlchemy implementation of doctor repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, doctor: Doctor) -> Doctor:
        """Create a new doctor."""
        from database.models import Doctor as DoctorModel

        db_doctor = DoctorModel(
            user_id=doctor.user_id,
            full_name=doctor.full_name,
            crm=doctor.crm,
            specialty=doctor.specialty,
            phone=doctor.phone,
            email=doctor.email,
            bio=doctor.bio,
            consultation_fee=doctor.consultation_fee,
            is_active=doctor.is_active,
        )
        self._session.add(db_doctor)
        await self._session.flush()
        await self._session.refresh(db_doctor)

        doctor.id = db_doctor.id
        return doctor

    async def get_by_id(self, doctor_id: int) -> Doctor | None:
        """Get doctor by ID."""
        from database.models import Doctor as DoctorModel

        result = await self._session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor_id)
        )
        db_doctor = result.scalar_one_or_none()

        if db_doctor is None:
            return None

        return self._to_entity(db_doctor)

    async def get_by_user_id(self, user_id: UUID) -> Doctor | None:
        """Get doctor by user ID."""
        from database.models import Doctor as DoctorModel

        result = await self._session.execute(
            select(DoctorModel).where(DoctorModel.user_id == user_id)
        )
        db_doctor = result.scalar_one_or_none()

        if db_doctor is None:
            return None

        return self._to_entity(db_doctor)

    async def get_by_crm(self, crm: str) -> Doctor | None:
        """Get doctor by CRM."""
        from database.models import Doctor as DoctorModel

        result = await self._session.execute(
            select(DoctorModel).where(DoctorModel.crm == crm.upper())
        )
        db_doctor = result.scalar_one_or_none()

        if db_doctor is None:
            return None

        return self._to_entity(db_doctor)

    async def update(self, doctor: Doctor) -> Doctor:
        """Update doctor."""
        from database.models import Doctor as DoctorModel

        result = await self._session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor.id)
        )
        db_doctor = result.scalar_one()

        db_doctor.full_name = doctor.full_name
        db_doctor.phone = doctor.phone
        db_doctor.bio = doctor.bio
        db_doctor.consultation_fee = doctor.consultation_fee
        db_doctor.is_active = doctor.is_active
        db_doctor.specialty = doctor.specialty

        await self._session.flush()
        await self._session.refresh(db_doctor)

        return doctor

    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors with optional filters."""
        from database.models import Doctor as DoctorModel

        query = select(DoctorModel)

        if filters:
            if "specialty" in filters:
                query = query.where(
                    DoctorModel.specialty.ilike(f"%{filters['specialty']}%")
                )
            if "is_active" in filters:
                query = query.where(
                    DoctorModel.is_active == filters["is_active"]
                )
            if "name" in filters:
                query = query.where(
                    DoctorModel.full_name.ilike(f"%{filters['name']}%")
                )

        query = query.where(DoctorModel.is_active == True)
        query = query.limit(limit).offset(offset)
        result = await self._session.execute(query)

        return [self._to_entity(d) for d in result.scalars().all()]

    async def list_by_specialty(
        self,
        specialty: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        """List doctors by specialty."""
        from database.models import Doctor as DoctorModel

        result = await self._session.execute(
            select(DoctorModel)
            .where(DoctorModel.specialty.ilike(f"%{specialty}%"))
            .where(DoctorModel.is_active == True)
            .limit(limit)
            .offset(offset)
        )

        return [self._to_entity(d) for d in result.scalars().all()]

    def _to_entity(self, db_doctor: Any) -> Doctor:
        """Convert database model to domain entity."""
        from decimal import Decimal

        return Doctor(
            id=db_doctor.id,
            user_id=db_doctor.user_id,
            full_name=db_doctor.full_name,
            crm=db_doctor.crm,
            specialty=db_doctor.specialty,
            phone=db_doctor.phone,
            email=db_doctor.email,
            bio=db_doctor.bio,
            consultation_fee=(
                Decimal(str(db_doctor.consultation_fee))
                if db_doctor.consultation_fee
                else None
            ),
            is_active=db_doctor.is_active,
        )
