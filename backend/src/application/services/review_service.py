"""Review service."""

from dataclasses import dataclass

from domain.entities import Review
from domain.exceptions import ReviewNotFoundError, ValidationError
from application.interfaces.repositories import ReviewRepository


@dataclass
class CreateReviewInput:
    """Input for creating a review."""
    doctor_id: int
    patient_id: int
    appointment_id: int
    rating: int
    comment: str | None = None
    is_anonymous: bool = False


@dataclass
class UpdateReviewInput:
    """Input for updating a review."""
    rating: int | None = None
    comment: str | None = None
    is_anonymous: bool | None = None


class ReviewService:
    """Review service."""

    def __init__(self, repository: ReviewRepository):
        self._repository = repository

    async def create_review(self, input_data: CreateReviewInput) -> Review:
        """Create a new review."""
        # Check if review already exists for appointment
        existing = await self._repository.get_by_appointment_id(
            input_data.appointment_id
        )
        if existing:
            raise ValidationError(
                f"Review already exists for appointment {input_data.appointment_id}"
            )

        review = Review(
            doctor_id=input_data.doctor_id,
            patient_id=input_data.patient_id,
            appointment_id=input_data.appointment_id,
            rating=input_data.rating,
            comment=input_data.comment,
            is_anonymous=input_data.is_anonymous,
        )

        return await self._repository.create(review)

    async def get_review(self, review_id: int) -> Review:
        """Get review by ID."""
        review = await self._repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundError(f"Review with ID {review_id} not found")
        return review

    async def update_review(
        self,
        review_id: int,
        input_data: UpdateReviewInput,
    ) -> Review:
        """Update review."""
        review = await self.get_review(review_id)

        if input_data.rating is not None:
            review.rating = input_data.rating
        if input_data.comment is not None:
            review.comment = input_data.comment
        if input_data.is_anonymous is not None:
            review.is_anonymous = input_data.is_anonymous

        return await self._repository.update(review)

    async def approve_review(self, review_id: int) -> Review:
        """Approve review (admin)."""
        review = await self.get_review(review_id)
        review.approve()
        return await self._repository.update(review)

    async def reject_review(self, review_id: int) -> Review:
        """Reject review (admin)."""
        review = await self.get_review(review_id)
        review.reject()
        return await self._repository.update(review)

    async def list_doctor_reviews(
        self,
        doctor_id: int,
        status: str = "approved",
        limit: int = 100,
        offset: int = 0,
    ) -> list[Review]:
        """List reviews for a doctor."""
        return await self._repository.list_by_doctor(
            doctor_id, status, limit, offset
        )

    async def get_doctor_rating(self, doctor_id: int) -> dict:
        """Get rating statistics for a doctor."""
        return await self._repository.calculate_doctor_rating(doctor_id)
