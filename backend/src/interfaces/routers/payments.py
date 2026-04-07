"""Payment routes."""

from typing import Annotated
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import PaymentService
from application.interfaces.repositories import PaymentRepository
from domain.exceptions import PaymentNotFoundError, ValidationError
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import SQLAlchemyPaymentRepository
from interfaces.schemas import ApiResponse

router = APIRouter(prefix="/payments", tags=["payments"])


async def get_payment_service():
    """Get payment service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyPaymentRepository(session)
        yield PaymentService(repository)


@router.post(
    "",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create payment intent",
)
async def create_payment_intent(
    appointment_id: int,
    patient_id: int,
    amount: Decimal,
    currency: str = "BRL",
    service: Annotated[PaymentService, Depends(get_payment_service)] = None,
):
    """Create a payment intent."""
    from application.services.payment_service import CreatePaymentInput
    
    try:
        input_data = CreatePaymentInput(
            appointment_id=appointment_id,
            patient_id=patient_id,
            amount=amount,
            currency=currency,
        )
        payment = await service.create_payment(input_data)
        return ApiResponse(data=payment.to_dict())
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get(
    "/{payment_id}",
    response_model=ApiResponse,
    summary="Get payment by ID",
)
async def get_payment(
    payment_id: int,
    service: Annotated[PaymentService, Depends(get_payment_service)] = None,
):
    """Get payment by ID."""
    try:
        payment = await service.get_payment(payment_id)
        return ApiResponse(data=payment.to_dict())
    except PaymentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{payment_id}/confirm",
    response_model=ApiResponse,
    summary="Confirm payment",
)
async def confirm_payment(
    payment_id: int,
    provider_payment_id: str,
    service: Annotated[PaymentService, Depends(get_payment_service)] = None,
):
    """Confirm a payment."""
    try:
        payment = await service.process_payment(payment_id, provider_payment_id)
        return ApiResponse(data=payment.to_dict())
    except PaymentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{payment_id}/refund",
    response_model=ApiResponse,
    summary="Refund payment",
)
async def refund_payment(
    payment_id: int,
    service: Annotated[PaymentService, Depends(get_payment_service)] = None,
):
    """Refund a payment."""
    try:
        payment = await service.refund_payment(payment_id)
        return ApiResponse(data=payment.to_dict())
    except PaymentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
