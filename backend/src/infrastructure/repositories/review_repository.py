"""Review repository implementation."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Review
from application.interfaces.repositories import ReviewRepository


class SQLAlchemyReviewRepository(ReviewRepository):
    """SQLAlchemy implementation of review repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, review: Review) -> Review:
        """Create a new review."""
        from database.models import Review as ReviewModel

        db_review = ReviewModel(
            doctor_id=review.doctor_id,
            patient_id=review.patient_id,
            appointment_id=review.appointment_id,
            rating=review.rating,
            comment=review.comment,
            is_anonymous=review.is_anonymous,
            status=review.status,
        )
        self._session.add(db_review)
        await self._session.flush()
        await self._session.refresh(db_review)

        review.id = db_review.id
        review.created_at = db_review.created_at
        review.updated_at = db_review.updated_at
        return review

    async def get_by_id(self, review_id: int) -> Review | None:
        """Get review by ID."""
        from database.models import Review as ReviewModel

        result = await self._session.execute(
            select(ReviewModel).where(ReviewModel.id == review_id)
        )
        db_review = result.scalar_one_or_none()

        if db_review is None:
            return None

        return self._to_entity(db_review)

    async def get_by_appointment_id(self, appointment_id: int) -> Review | None:
        """Get review by appointment ID."""
        from database.models import Review as ReviewModel

        result = await self._session.execute(
            select(ReviewModel).where(ReviewModel.appointment_id == appointment_id)
        )
        db_review = result.scalar_one_or_none()

        if db_review is None:
            return None

        return self._to_entity(db_review)

    async def update(self, review: Review) -> Review:
        """Update review."""
        from database.models import Review as ReviewModel

        result = await self._session.execute(
            select(ReviewModel).where(ReviewModel.id == review.id)
        )
        db_review = result.scalar_one()

        db_review.rating = review.rating
        db_review.comment = review.comment
        db_review.is_anonymous = review.is_anonymous
        db_review.status = review.status

        await self._session.flush()
        await self._session.refresh(db_review)

        review.updated_at = db_review.updated_at
        return review

    async def list_by_doctor(
        self,
        doctor_id: int,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Review]:
        """List reviews by doctor."""
        from database.models import Review as ReviewModel

        query = select(ReviewModel).where(ReviewModel.doctor_id == doctor_id)
        
        if status:
            query = query.where(ReviewModel.status == status)
        
        query = (
            query.order_by(ReviewModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self._session.execute(query)
        return [self._to_entity(r) for r in result.scalars().all()]

    async def calculate_doctor_rating(self, doctor_id: int) -> dict:
        """Calculate rating statistics for a doctor."""
        from database.models import Review as ReviewModel

        result = await self._session.execute(
            select(
                func.avg(ReviewModel.rating).label("average"),
                func.count(ReviewModel.id).label("total"),
            )
            .where(ReviewModel.doctor_id == doctor_id)
            .where(ReviewModel.status == "approved")
        )
        
        row = result.one()
        return {
            "average": float(row.average) if row.average else 0.0,
            "total": row.total,
        }

    def _to_entity(self, db_review) -> Review:
        """Convert database model to domain entity."""
        return Review(
            id=db_review.id,
            doctor_id=db_review.doctor_id,
            patient_id=db_review.patient_id,
            appointment_id=db_review.appointment_id,
            rating=db_review.rating,
            comment=db_review.comment,
            is_anonymous=db_review.is_anonymous,
            status=db_review.status,
            created_at=db_review.created_at,
            updated_at=db_review.updated_at,
        )
