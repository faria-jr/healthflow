"""Notification models."""

from typing import Any
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class NotificationPreference(Base, TimestampMixin):
    """User notification preferences."""
    
    __tablename__ = "notification_preferences"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    email_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sms_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    push_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    reminder_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    
    __table_args__ = (
        {"comment": "User notification preferences"},
    )
    
    def __repr__(self) -> str:
        return f"<NotificationPreference(user_id={self.user_id})>"


class Notification(Base):
    """Notification entity."""
    
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(Text, nullable=False)  # email, sms, push
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True, default=dict)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="pending")  # pending, sent, failed, read
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    
    __table_args__ = (
        {"comment": "Notifications sent to users"},
    )
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.type}, status={self.status})>"
