"""Review routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import ReviewService
from application.interfaces.repositories import ReviewRepository
from domain.exceptions import ReviewNotFoundError, ValidationError
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import SQLAlchemyReviewRepository
from interfaces.schemas import ApiResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])


async def get_review_service():
    """Get review service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyReviewRepository(session)
        yield ReviewService(repository)


@router.post(
    "",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create review",
)
async def create_review(
    doctor_id: int,
    patient_id: int,
    appointment_id: int,
    rating: int,
    comment: str | None = None,
    is_anonymous: bool = False,
    service: Annotated[ReviewService, Depends(get_review_service)] = None,
):
    """Create a new review."""
    from application.services.review_service import CreateReviewInput
    
    try:
        input_data = CreateReviewInput(
            doctor_id=doctor_id,
            patient_id=patient_id,
            appointment_id=appointment_id,
            rating=rating,
            comment=comment,
            is_anonymous=is_anonymous,
        )
        review = await service.create_review(input_data)
        return ApiResponse(data=review.to_dict())
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get(
    "/{review_id}",
    response_model=ApiResponse,
    summary="Get review by ID",
)
async def get_review(
    review_id: int,
    service: Annotated[ReviewService, Depends(get_review_service)] = None,
):
    """Get review by ID."""
    try:
        review = await service.get_review(review_id)
        return ApiResponse(data=review.to_dict())
    except ReviewNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/doctor/{doctor_id}",
    response_model=ApiResponse,
    summary="List doctor reviews",
)
async def list_doctor_reviews(
    doctor_id: int,
    status: str = "approved",
    limit: int = 100,
    offset: int = 0,
    service: Annotated[ReviewService, Depends(get_review_service)] = None,
):
    """List reviews for a doctor."""
    reviews = await service.list_doctor_reviews(doctor_id, status, limit, offset)
    return ApiResponse(data={"reviews": [r.to_dict() for r in reviews]})


@router.get(
    "/doctor/{doctor_id}/rating",
    response_model=ApiResponse,
    summary="Get doctor rating",
)
async def get_doctor_rating(
    doctor_id: int,
    service: Annotated[ReviewService, Depends(get_review_service)] = None,
):
    """Get rating statistics for a doctor."""
    rating = await service.get_doctor_rating(doctor_id)
    return ApiResponse(data=rating)


@router.patch(
    "/{review_id}/moderate",
    response_model=ApiResponse,
    summary="Moderate review (admin)",
)
async def moderate_review(
    review_id: int,
    action: str,  # approve, reject
    service: Annotated[ReviewService, Depends(get_review_service)] = None,
):
    """Moderate a review (approve/reject)."""
    try:
        if action == "approve":
            review = await service.approve_review(review_id)
        elif action == "reject":
            review = await service.reject_review(review_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action must be 'approve' or 'reject'",
            )
        return ApiResponse(data=review.to_dict())
    except ReviewNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
