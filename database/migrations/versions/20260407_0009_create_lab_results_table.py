"""create lab results table

Revision ID: 0009
Revises: 0008
Create Date: 2026-04-07 13:21:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lab_results",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "patient_id",
            sa.BigInteger(),
            sa.ForeignKey("patients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "doctor_id",
            sa.BigInteger(),
            sa.ForeignKey("doctors.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "appointment_id",
            sa.BigInteger(),
            sa.ForeignKey("appointments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "lab_name",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "test_type",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "result_summary",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "file_url",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "file_name",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "file_size",
            sa.BigInteger(),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
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
        sa.PrimaryKeyConstraint("id", name="pk_lab_results"),
        sa.CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed')",
            name="ck_lab_results_status",
        ),
    )
    
    op.create_index("ix_lab_results_patient_id", "lab_results", ["patient_id"])
    op.create_index("ix_lab_results_doctor_id", "lab_results", ["doctor_id"])
    op.create_index("ix_lab_results_appointment_id", "lab_results", ["appointment_id"])
    op.create_index("ix_lab_results_status", "lab_results", ["status"])
    op.create_index("ix_lab_results_uploaded_at", "lab_results", ["uploaded_at"])


def downgrade() -> None:
    op.drop_index("ix_lab_results_uploaded_at", table_name="lab_results")
    op.drop_index("ix_lab_results_status", table_name="lab_results")
    op.drop_index("ix_lab_results_appointment_id", table_name="lab_results")
    op.drop_index("ix_lab_results_doctor_id", table_name="lab_results")
    op.drop_index("ix_lab_results_patient_id", table_name="lab_results")
    op.drop_table("lab_results")
