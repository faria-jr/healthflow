"""create patients table

Revision ID: 0001
Revises:
Create Date: 2026-04-06 19:50:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("auth.users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("cpf", sa.Text(), nullable=False),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("gender", sa.Text(), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("emergency_contact", postgresql.JSONB(), nullable=True),
        sa.Column(
            "medical_history",
            postgresql.JSONB(),
            nullable=True,
            server_default="{}",
        ),
        sa.Column(
            "allergies",
            postgresql.JSONB(),
            nullable=True,
            server_default="[]",
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
        sa.PrimaryKeyConstraint("id", name="pk_patients"),
        sa.UniqueConstraint("cpf", name="uq_patients_cpf"),
        sa.UniqueConstraint("email", name="uq_patients_email"),
        sa.UniqueConstraint("user_id", name="uq_patients_user_id"),
    )

    # Indexes
    op.create_index("ix_patients_user_id", "patients", ["user_id"])
    op.create_index("ix_patients_cpf", "patients", ["cpf"])
    op.create_index("ix_patients_email", "patients", ["email"])
    op.create_index("ix_patients_full_name", "patients", ["full_name"])


def downgrade() -> None:
    op.drop_index("ix_patients_full_name", table_name="patients")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_index("ix_patients_cpf", table_name="patients")
    op.drop_index("ix_patients_user_id", table_name="patients")
    op.drop_table("patients")
