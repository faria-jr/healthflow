"""create payments table

Revision ID: 0006
Revises: 0005
Create Date: 2026-04-07 12:46:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "appointment_id",
            sa.BigInteger(),
            sa.ForeignKey("appointments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "patient_id",
            sa.BigInteger(),
            sa.ForeignKey("patients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(10, 2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.Text(),
            nullable=False,
            server_default="BRL",
        ),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "provider",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "provider_payment_id",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "paid_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "refunded_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_payments"),
        sa.UniqueConstraint(
            "appointment_id",
            name="uq_payments_appointment_id",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed', 'refunded')",
            name="ck_payments_status",
        ),
        sa.CheckConstraint(
            "amount > 0",
            name="ck_payments_amount_positive",
        ),
    )
    
    op.create_index("ix_payments_appointment_id", "payments", ["appointment_id"])
    op.create_index("ix_payments_patient_id", "payments", ["patient_id"])
    op.create_index("ix_payments_status", "payments", ["status"])
    op.create_index("ix_payments_provider_payment_id", "payments", ["provider_payment_id"])


def downgrade() -> None:
    op.drop_index("ix_payments_provider_payment_id", table_name="payments")
    op.drop_index("ix_payments_status", table_name="payments")
    op.drop_index("ix_payments_patient_id", table_name="payments")
    op.drop_index("ix_payments_appointment_id", table_name="payments")
    op.drop_table("payments")
