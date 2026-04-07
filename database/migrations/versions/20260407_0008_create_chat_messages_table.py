"""create chat messages table

Revision ID: 0008
Revises: 0007
Create Date: 2026-04-07 13:20:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_messages",
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
            "sender_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "sender_type",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "attachments",
            postgresql.JSONB(),
            nullable=True,
            server_default="[]",
        ),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "read_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_chat_messages"),
        sa.CheckConstraint(
            "sender_type IN ('patient', 'doctor')",
            name="ck_chat_messages_sender_type",
        ),
    )
    
    op.create_index("ix_chat_messages_appointment_id", "chat_messages", ["appointment_id"])
    op.create_index("ix_chat_messages_sender_id", "chat_messages", ["sender_id"])
    op.create_index("ix_chat_messages_sent_at", "chat_messages", ["sent_at"])
    op.create_index("ix_chat_messages_appointment_sent", "chat_messages", ["appointment_id", "sent_at"])


def downgrade() -> None:
    op.drop_index("ix_chat_messages_appointment_sent", table_name="chat_messages")
    op.drop_index("ix_chat_messages_sent_at", table_name="chat_messages")
    op.drop_index("ix_chat_messages_sender_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_appointment_id", table_name="chat_messages")
    op.drop_table("chat_messages")
