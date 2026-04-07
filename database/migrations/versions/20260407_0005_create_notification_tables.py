"""create notification tables

Revision ID: 0005
Revises: 0004
Create Date: 2026-04-07 12:45:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # notification_preferences
    op.create_table(
        "notification_preferences",
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
        sa.Column(
            "email_enabled",
            sa.Boolean(),
            nullable=False,
            server_default="true",
        ),
        sa.Column(
            "sms_enabled",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.Column(
            "push_enabled",
            sa.Boolean(),
            nullable=False,
            server_default="true",
        ),
        sa.Column(
            "reminder_hours",
            sa.Integer(),
            nullable=False,
            server_default="24",
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
        sa.PrimaryKeyConstraint("id", name="pk_notification_preferences"),
        sa.UniqueConstraint("user_id", name="uq_notification_preferences_user_id"),
    )
    
    op.create_index("ix_notification_preferences_user_id", "notification_preferences", ["user_id"])

    # notifications
    op.create_table(
        "notifications",
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
        sa.Column(
            "type",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "body",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "data",
            postgresql.JSONB(),
            nullable=True,
            server_default="{}",
        ),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "read_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_notifications"),
        sa.CheckConstraint(
            "type IN ('email', 'sms', 'push')",
            name="ck_notifications_type",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'read')",
            name="ck_notifications_status",
        ),
    )
    
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_notifications_status", "notifications", ["status"])
    op.create_index("ix_notifications_created_at", "notifications", ["created_at"])
    op.create_index("ix_notifications_user_status", "notifications", ["user_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_notifications_user_status", table_name="notifications")
    op.drop_index("ix_notifications_created_at", table_name="notifications")
    op.drop_index("ix_notifications_status", table_name="notifications")
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")
    
    op.drop_index("ix_notification_preferences_user_id", table_name="notification_preferences")
    op.drop_table("notification_preferences")
