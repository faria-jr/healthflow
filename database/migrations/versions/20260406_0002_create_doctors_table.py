"""create doctors table

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-06 19:51:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "doctors",
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
        sa.Column("crm", sa.Text(), nullable=False),
        sa.Column("specialty", sa.Text(), nullable=False),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("consultation_fee", sa.Numeric(10, 2), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default="true",
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
        sa.PrimaryKeyConstraint("id", name="pk_doctors"),
        sa.UniqueConstraint("crm", name="uq_doctors_crm"),
        sa.UniqueConstraint("email", name="uq_doctors_email"),
        sa.UniqueConstraint("user_id", name="uq_doctors_user_id"),
    )

    # Indexes
    op.create_index("ix_doctors_user_id", "doctors", ["user_id"])
    op.create_index("ix_doctors_crm", "doctors", ["crm"])
    op.create_index("ix_doctors_specialty", "doctors", ["specialty"])
    op.create_index("ix_doctors_is_active", "doctors", ["is_active"])
    op.create_index(
        "ix_doctors_specialty_active",
        "doctors",
        ["specialty", "is_active"],
    )


def downgrade() -> None:
    op.drop_index("ix_doctors_specialty_active", table_name="doctors")
    op.drop_index("ix_doctors_is_active", table_name="doctors")
    op.drop_index("ix_doctors_specialty", table_name="doctors")
    op.drop_index("ix_doctors_crm", table_name="doctors")
    op.drop_index("ix_doctors_user_id", table_name="doctors")
    op.drop_table("doctors")
