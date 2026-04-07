"""Chat message repository implementation."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import ChatMessage
from application.interfaces.repositories import ChatMessageRepository


class SQLAlchemyChatMessageRepository(ChatMessageRepository):
    """SQLAlchemy implementation of chat message repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, message: ChatMessage) -> ChatMessage:
        """Create a new chat message."""
        from database.models import ChatMessage as ChatMessageModel

        db_message = ChatMessageModel(
            appointment_id=message.appointment_id,
            sender_id=message.sender_id,
            sender_type=message.sender_type,
            content=message.content,
            attachments=message.attachments,
        )
        self._session.add(db_message)
        await self._session.flush()
        await self._session.refresh(db_message)

        message.id = db_message.id
        message.sent_at = db_message.sent_at
        return message

    async def get_by_id(self, message_id: int) -> ChatMessage | None:
        """Get message by ID."""
        from database.models import ChatMessage as ChatMessageModel

        result = await self._session.execute(
            select(ChatMessageModel).where(ChatMessageModel.id == message_id)
        )
        db_message = result.scalar_one_or_none()

        if db_message is None:
            return None

        return self._to_entity(db_message)

    async def update(self, message: ChatMessage) -> ChatMessage:
        """Update message."""
        from database.models import ChatMessage as ChatMessageModel

        result = await self._session.execute(
            select(ChatMessageModel).where(ChatMessageModel.id == message.id)
        )
        db_message = result.scalar_one()

        db_message.read_at = message.read_at

        await self._session.flush()
        await self._session.refresh(db_message)

        return message

    async def list_by_appointment(
        self,
        appointment_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ChatMessage]:
        """List messages by appointment."""
        from database.models import ChatMessage as ChatMessageModel

        result = await self._session.execute(
            select(ChatMessageModel)
            .where(ChatMessageModel.appointment_id == appointment_id)
            .order_by(ChatMessageModel.sent_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def count_unread(
        self,
        appointment_id: int,
        user_id: UUID,
    ) -> int:
        """Count unread messages for user in appointment."""
        from database.models import ChatMessage as ChatMessageModel

        result = await self._session.execute(
            select(ChatMessageModel)
            .where(ChatMessageModel.appointment_id == appointment_id)
            .where(ChatMessageModel.sender_id != user_id)
            .where(ChatMessageModel.read_at.is_(None))
        )
        return len(result.scalars().all())

    def _to_entity(self, db_message) -> ChatMessage:
        """Convert database model to domain entity."""
        return ChatMessage(
            id=db_message.id,
            appointment_id=db_message.appointment_id,
            sender_id=db_message.sender_id,
            sender_type=db_message.sender_type,
            content=db_message.content,
            attachments=db_message.attachments or [],
            sent_at=db_message.sent_at,
            read_at=db_message.read_at,
        )
