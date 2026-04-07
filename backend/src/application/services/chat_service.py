"""Chat service."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities import ChatMessage
from domain.exceptions import ChatMessageNotFoundError, ValidationError
from application.interfaces.repositories import ChatMessageRepository


@dataclass
class SendMessageInput:
    """Input for sending a chat message."""
    appointment_id: int
    sender_id: UUID
    sender_type: str  # patient, doctor
    content: str
    attachments: list[dict[str, Any]] | None = None


class ChatService:
    """Chat service."""

    def __init__(self, repository: ChatMessageRepository):
        self._repository = repository

    async def send_message(self, input_data: SendMessageInput) -> ChatMessage:
        """Send a chat message."""
        message = ChatMessage(
            appointment_id=input_data.appointment_id,
            sender_id=input_data.sender_id,
            sender_type=input_data.sender_type,
            content=input_data.content,
            attachments=input_data.attachments or [],
        )
        return await self._repository.create(message)

    async def get_message(self, message_id: int) -> ChatMessage:
        """Get message by ID."""
        message = await self._repository.get_by_id(message_id)
        if not message:
            raise ChatMessageNotFoundError(
                f"Message with ID {message_id} not found"
            )
        return message

    async def mark_as_read(self, message_id: int) -> ChatMessage:
        """Mark message as read."""
        message = await self.get_message(message_id)
        message.mark_as_read()
        return await self._repository.update(message)

    async def list_appointment_messages(
        self,
        appointment_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ChatMessage]:
        """List messages for an appointment."""
        return await self._repository.list_by_appointment(
            appointment_id, limit, offset
        )

    async def get_unread_count(
        self,
        appointment_id: int,
        user_id: UUID,
    ) -> int:
        """Get count of unread messages for user in appointment."""
        return await self._repository.count_unread(appointment_id, user_id)
