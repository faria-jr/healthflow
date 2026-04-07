"""Payment service."""

from dataclasses import dataclass
from decimal import Decimal

from domain.entities import Payment
from domain.exceptions import PaymentNotFoundError, ValidationError
from application.interfaces.repositories import PaymentRepository


@dataclass
class CreatePaymentInput:
    """Input for creating a payment."""
    appointment_id: int
    patient_id: int
    amount: Decimal
    currency: str = "BRL"
    provider: str = "stripe"


@dataclass
class ProcessPaymentInput:
    """Input for processing a payment."""
    payment_id: int
    provider_payment_id: str


class PaymentService:
    """Payment service."""

    def __init__(self, repository: PaymentRepository):
        self._repository = repository

    async def create_payment(self, input_data: CreatePaymentInput) -> Payment:
        """Create a new payment."""
        # Check if payment already exists for appointment
        existing = await self._repository.get_by_appointment_id(
            input_data.appointment_id
        )
        if existing:
            raise ValidationError(
                f"Payment already exists for appointment {input_data.appointment_id}"
            )

        payment = Payment(
            appointment_id=input_data.appointment_id,
            patient_id=input_data.patient_id,
            amount=input_data.amount,
            currency=input_data.currency,
            provider=input_data.provider,
        )

        return await self._repository.create(payment)

    async def get_payment(self, payment_id: int) -> Payment:
        """Get payment by ID."""
        payment = await self._repository.get_by_id(payment_id)
        if not payment:
            raise PaymentNotFoundError(f"Payment with ID {payment_id} not found")
        return payment

    async def get_payment_by_appointment(self, appointment_id: int) -> Payment:
        """Get payment by appointment ID."""
        payment = await self._repository.get_by_appointment_id(appointment_id)
        if not payment:
            raise PaymentNotFoundError(
                f"Payment for appointment {appointment_id} not found"
            )
        return payment

    async def process_payment(
        self,
        payment_id: int,
        provider_payment_id: str,
    ) -> Payment:
        """Process a payment."""
        payment = await self.get_payment(payment_id)
        
        payment.mark_as_processing()
        payment.provider_payment_id = provider_payment_id
        
        # In real implementation, verify with provider here
        payment.mark_as_completed()
        
        return await self._repository.update(payment)

    async def refund_payment(self, payment_id: int) -> Payment:
        """Refund a payment."""
        payment = await self.get_payment(payment_id)
        payment.refund()
        return await self._repository.update(payment)
