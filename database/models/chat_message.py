"""Chat message model."""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ChatMessage(Base):
    """Chat message entity."""
    
    __tablename__ = "chat_messages"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    appointment_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    sender_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )  # patient, doctor
    content: Mapped[str] = mapped_column(Text, nullable=False)
    attachments: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB,
        nullable=True,
        default=list,
    )
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"comment": "Chat messages for appointments"},
    )
    
    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id}, appointment_id={self.appointment_id})>"
