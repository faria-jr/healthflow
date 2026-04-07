"""create reviews table

Revision ID: 0007
Revises: 0006
Create Date: 2026-04-07 12:47:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "doctor_id",
            sa.BigInteger(),
            sa.ForeignKey("doctors.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "patient_id",
            sa.BigInteger(),
            sa.ForeignKey("patients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "appointment_id",
            sa.BigInteger(),
            sa.ForeignKey("appointments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "rating",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "comment",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "is_anonymous",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="pending",
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
        sa.PrimaryKeyConstraint("id", name="pk_reviews"),
        sa.UniqueConstraint(
            "appointment_id",
            name="uq_reviews_appointment_id",
        ),
        sa.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_reviews_rating_range",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="ck_reviews_status",
        ),
    )
    
    op.create_index("ix_reviews_doctor_id", "reviews", ["doctor_id"])
    op.create_index("ix_reviews_patient_id", "reviews", ["patient_id"])
    op.create_index("ix_reviews_appointment_id", "reviews", ["appointment_id"])
    op.create_index("ix_reviews_status", "reviews", ["status"])
    op.create_index("ix_reviews_doctor_status", "reviews", ["doctor_id", "status"])
    op.create_index("ix_reviews_created_at", "reviews", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_reviews_created_at", table_name="reviews")
    op.drop_index("ix_reviews_doctor_status", table_name="reviews")
    op.drop_index("ix_reviews_status", table_name="reviews")
    op.drop_index("ix_reviews_appointment_id", table_name="reviews")
    op.drop_index("ix_reviews_patient_id", table_name="reviews")
    op.drop_index("ix_reviews_doctor_id", table_name="reviews")
    op.drop_table("reviews")
