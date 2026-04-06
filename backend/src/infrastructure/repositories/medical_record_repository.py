"""Medical record repository implementation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import MedicalRecord
from application.interfaces.repositories import MedicalRecordRepository


class SQLAlchemyMedicalRecordRepository(MedicalRecordRepository):
    """SQLAlchemy implementation of medical record repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, record: MedicalRecord) -> MedicalRecord:
        """Create a new medical record."""
        from database.models import MedicalRecord as MedicalRecordModel

        db_record = MedicalRecordModel(
            appointment_id=record.appointment_id,
            patient_id=record.patient_id,
            doctor_id=record.doctor_id,
            diagnosis=record.diagnosis,
            symptoms=record.symptoms,
            prescription=record.prescription,
            notes=record.notes,
            attachments=record.attachments,
        )
        self._session.add(db_record)
        await self._session.flush()
        await self._session.refresh(db_record)

        record.id = db_record.id
        record.created_at = db_record.created_at
        record.updated_at = db_record.updated_at
        return record

    async def get_by_id(self, record_id: int) -> MedicalRecord | None:
        """Get medical record by ID."""
        from database.models import MedicalRecord as MedicalRecordModel

        result = await self._session.execute(
            select(MedicalRecordModel).where(
                MedicalRecordModel.id == record_id
            )
        )
        db_record = result.scalar_one_or_none()

        if db_record is None:
            return None

        return self._to_entity(db_record)

    async def get_by_appointment_id(
        self, appointment_id: int
    ) -> MedicalRecord | None:
        """Get medical record by appointment ID."""
        from database.models import MedicalRecord as MedicalRecordModel

        result = await self._session.execute(
            select(MedicalRecordModel).where(
                MedicalRecordModel.appointment_id == appointment_id
            )
        )
        db_record = result.scalar_one_or_none()

        if db_record is None:
            return None

        return self._to_entity(db_record)

    async def update(self, record: MedicalRecord) -> MedicalRecord:
        """Update medical record."""
        from database.models import MedicalRecord as MedicalRecordModel

        result = await self._session.execute(
            select(MedicalRecordModel).where(
                MedicalRecordModel.id == record.id
            )
        )
        db_record = result.scalar_one()

        db_record.diagnosis = record.diagnosis
        db_record.symptoms = record.symptoms
        db_record.prescription = record.prescription
        db_record.notes = record.notes
        db_record.attachments = record.attachments

        await self._session.flush()
        await self._session.refresh(db_record)

        record.updated_at = db_record.updated_at
        return record

    async def list_by_patient(
        self,
        patient_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records by patient."""
        from database.models import MedicalRecord as MedicalRecordModel

        result = await self._session.execute(
            select(MedicalRecordModel)
            .where(MedicalRecordModel.patient_id == patient_id)
            .order_by(MedicalRecordModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return [self._to_entity(r) for r in result.scalars().all()]

    async def list_by_doctor(
        self,
        doctor_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MedicalRecord]:
        """List medical records by doctor."""
        from database.models import MedicalRecord as MedicalRecordModel

        result = await self._session.execute(
            select(MedicalRecordModel)
            .where(MedicalRecordModel.doctor_id == doctor_id)
            .order_by(MedicalRecordModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return [self._to_entity(r) for r in result.scalars().all()]

    def _to_entity(self, db_record: Any) -> MedicalRecord:
        """Convert database model to domain entity."""
        return MedicalRecord(
            id=db_record.id,
            appointment_id=db_record.appointment_id,
            patient_id=db_record.patient_id,
            doctor_id=db_record.doctor_id,
            diagnosis=db_record.diagnosis,
            symptoms=db_record.symptoms,
            prescription=db_record.prescription,
            notes=db_record.notes,
            attachments=db_record.attachments or [],
            created_at=db_record.created_at,
            updated_at=db_record.updated_at,
        )
