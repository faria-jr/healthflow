"""create medical_records table

Revision ID: 0004
Revises: 0003
Create Date: 2026-04-06 19:53:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "medical_records",
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
            "doctor_id",
            sa.BigInteger(),
            sa.ForeignKey("doctors.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("diagnosis", sa.Text(), nullable=True),
        sa.Column("symptoms", sa.Text(), nullable=True),
        sa.Column("prescription", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "attachments",
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
        sa.PrimaryKeyConstraint("id", name="pk_medical_records"),
        sa.UniqueConstraint(
            "appointment_id",
            name="uq_medical_records_appointment_id",
        ),
    )

    # Indexes
    op.create_index(
        "ix_medical_records_appointment_id",
        "medical_records",
        ["appointment_id"],
    )
    op.create_index(
        "ix_medical_records_patient_id",
        "medical_records",
        ["patient_id"],
    )
    op.create_index(
        "ix_medical_records_doctor_id",
        "medical_records",
        ["doctor_id"],
    )
    op.create_index(
        "ix_medical_records_created_at",
        "medical_records",
        ["created_at"],
    )
    op.create_index(
        "ix_medical_records_patient_created",
        "medical_records",
        ["patient_id", "created_at"],
    )
    op.create_index(
        "ix_medical_records_doctor_created",
        "medical_records",
        ["doctor_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_medical_records_doctor_created", table_name="medical_records")
    op.drop_index("ix_medical_records_patient_created", table_name="medical_records")
    op.drop_index("ix_medical_records_created_at", table_name="medical_records")
    op.drop_index("ix_medical_records_doctor_id", table_name="medical_records")
    op.drop_index("ix_medical_records_patient_id", table_name="medical_records")
    op.drop_index("ix_medical_records_appointment_id", table_name="medical_records")
    op.drop_table("medical_records")
