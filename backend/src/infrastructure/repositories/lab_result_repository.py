"""Lab result repository implementation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import LabResult
from application.interfaces.repositories import LabResultRepository


class SQLAlchemyLabResultRepository(LabResultRepository):
    """SQLAlchemy implementation of lab result repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, lab_result: LabResult) -> LabResult:
        """Create a new lab result."""
        from database.models import LabResult as LabResultModel

        db_result = LabResultModel(
            patient_id=lab_result.patient_id,
            doctor_id=lab_result.doctor_id,
            appointment_id=lab_result.appointment_id,
            lab_name=lab_result.lab_name,
            test_type=lab_result.test_type,
            result_summary=lab_result.result_summary,
            file_url=lab_result.file_url,
            file_name=lab_result.file_name,
            file_size=lab_result.file_size,
            status=lab_result.status,
        )
        self._session.add(db_result)
        await self._session.flush()
        await self._session.refresh(db_result)

        lab_result.id = db_result.id
        lab_result.created_at = db_result.created_at
        lab_result.updated_at = db_result.updated_at
        return lab_result

    async def get_by_id(self, lab_result_id: int) -> LabResult | None:
        """Get lab result by ID."""
        from database.models import LabResult as LabResultModel

        result = await self._session.execute(
            select(LabResultModel).where(LabResultModel.id == lab_result_id)
        )
        db_result = result.scalar_one_or_none()

        if db_result is None:
            return None

        return self._to_entity(db_result)

    async def update(self, lab_result: LabResult) -> LabResult:
        """Update lab result."""
        from database.models import LabResult as LabResultModel

        result = await self._session.execute(
            select(LabResultModel).where(LabResultModel.id == lab_result.id)
        )
        db_result = result.scalar_one()

        db_result.result_summary = lab_result.result_summary
        db_result.file_url = lab_result.file_url
        db_result.file_name = lab_result.file_name
        db_result.file_size = lab_result.file_size
        db_result.status = lab_result.status

        await self._session.flush()
        await self._session.refresh(db_result)

        lab_result.updated_at = db_result.updated_at
        return lab_result

    async def list_by_patient(
        self,
        patient_id: int,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[LabResult]:
        """List lab results by patient."""
        from database.models import LabResult as LabResultModel

        query = select(LabResultModel).where(LabResultModel.patient_id == patient_id)
        
        if status:
            query = query.where(LabResultModel.status == status)
        
        query = (
            query.order_by(LabResultModel.uploaded_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self._session.execute(query)
        return [self._to_entity(r) for r in result.scalars().all()]

    async def list_by_doctor(
        self,
        doctor_id: int,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[LabResult]:
        """List lab results by doctor."""
        from database.models import LabResult as LabResultModel

        query = select(LabResultModel).where(LabResultModel.doctor_id == doctor_id)
        
        if status:
            query = query.where(LabResultModel.status == status)
        
        query = (
            query.order_by(LabResultModel.uploaded_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self._session.execute(query)
        return [self._to_entity(r) for r in result.scalars().all()]

    def _to_entity(self, db_result) -> LabResult:
        """Convert database model to domain entity."""
        return LabResult(
            id=db_result.id,
            patient_id=db_result.patient_id,
            doctor_id=db_result.doctor_id,
            appointment_id=db_result.appointment_id,
            lab_name=db_result.lab_name,
            test_type=db_result.test_type,
            result_summary=db_result.result_summary,
            file_url=db_result.file_url,
            file_name=db_result.file_name,
            file_size=db_result.file_size,
            status=db_result.status,
            uploaded_at=db_result.uploaded_at,
            created_at=db_result.created_at,
            updated_at=db_result.updated_at,
        )
