"""Payment repository implementation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Payment
from application.interfaces.repositories import PaymentRepository


class SQLAlchemyPaymentRepository(PaymentRepository):
    """SQLAlchemy implementation of payment repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        from database.models import Payment as PaymentModel

        db_payment = PaymentModel(
            appointment_id=payment.appointment_id,
            patient_id=payment.patient_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status,
            provider=payment.provider,
            provider_payment_id=payment.provider_payment_id,
        )
        self._session.add(db_payment)
        await self._session.flush()
        await self._session.refresh(db_payment)

        payment.id = db_payment.id
        payment.created_at = db_payment.created_at
        payment.updated_at = db_payment.updated_at
        return payment

    async def get_by_id(self, payment_id: int) -> Payment | None:
        """Get payment by ID."""
        from database.models import Payment as PaymentModel

        result = await self._session.execute(
            select(PaymentModel).where(PaymentModel.id == payment_id)
        )
        db_payment = result.scalar_one_or_none()

        if db_payment is None:
            return None

        return self._to_entity(db_payment)

    async def get_by_appointment_id(self, appointment_id: int) -> Payment | None:
        """Get payment by appointment ID."""
        from database.models import Payment as PaymentModel

        result = await self._session.execute(
            select(PaymentModel).where(PaymentModel.appointment_id == appointment_id)
        )
        db_payment = result.scalar_one_or_none()

        if db_payment is None:
            return None

        return self._to_entity(db_payment)

    async def update(self, payment: Payment) -> Payment:
        """Update payment."""
        from database.models import Payment as PaymentModel

        result = await self._session.execute(
            select(PaymentModel).where(PaymentModel.id == payment.id)
        )
        db_payment = result.scalar_one()

        db_payment.status = payment.status
        db_payment.provider_payment_id = payment.provider_payment_id
        db_payment.paid_at = payment.paid_at
        db_payment.refunded_at = payment.refunded_at

        await self._session.flush()
        await self._session.refresh(db_payment)

        payment.updated_at = db_payment.updated_at
        return payment

    def _to_entity(self, db_payment) -> Payment:
        """Convert database model to domain entity."""
        from decimal import Decimal

        return Payment(
            id=db_payment.id,
            appointment_id=db_payment.appointment_id,
            patient_id=db_payment.patient_id,
            amount=Decimal(str(db_payment.amount)),
            currency=db_payment.currency,
            status=db_payment.status,
            provider=db_payment.provider,
            provider_payment_id=db_payment.provider_payment_id,
            paid_at=db_payment.paid_at,
            refunded_at=db_payment.refunded_at,
            created_at=db_payment.created_at,
            updated_at=db_payment.updated_at,
        )
