"""create appointments table

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-06 19:52:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "appointments",
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
            sa.ForeignKey("doctors.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "scheduled_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "duration_minutes",
            sa.Integer(),
            nullable=False,
            server_default="30",
        ),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="scheduled",
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(),
            nullable=True,
            server_default="{}",
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
        sa.PrimaryKeyConstraint("id", name="pk_appointments"),
        sa.CheckConstraint(
            "status IN ('scheduled', 'confirmed', 'completed', 'cancelled', 'no_show')",
            name="ck_appointments_status",
        ),
        sa.CheckConstraint(
            "duration_minutes > 0",
            name="ck_appointments_duration_positive",
        ),
    )

    # Indexes
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_scheduled_at", "appointments", ["scheduled_at"])
    op.create_index("ix_appointments_status", "appointments", ["status"])
    op.create_index(
        "ix_appointments_patient_scheduled",
        "appointments",
        ["patient_id", "scheduled_at"],
    )
    op.create_index(
        "ix_appointments_doctor_scheduled",
        "appointments",
        ["doctor_id", "scheduled_at"],
    )
    op.create_index(
        "ix_appointments_doctor_time_range",
        "appointments",
        ["doctor_id", "scheduled_at", "duration_minutes"],
    )
    op.create_index(
        "ix_appointments_status_scheduled",
        "appointments",
        ["status"],
        postgresql_where=sa.text("status IN ('scheduled', 'confirmed')"),
    )


def downgrade() -> None:
    op.drop_index("ix_appointments_status_scheduled", table_name="appointments")
    op.drop_index("ix_appointments_doctor_time_range", table_name="appointments")
    op.drop_index("ix_appointments_doctor_scheduled", table_name="appointments")
    op.drop_index("ix_appointments_patient_scheduled", table_name="appointments")
    op.drop_index("ix_appointments_status", table_name="appointments")
    op.drop_index("ix_appointments_scheduled_at", table_name="appointments")
    op.drop_index("ix_appointments_doctor_id", table_name="appointments")
    op.drop_index("ix_appointments_patient_id", table_name="appointments")
    op.drop_table("appointments")
