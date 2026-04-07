"""Notification repository implementation."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Notification, NotificationPreference
from application.interfaces.repositories import NotificationRepository


class SQLAlchemyNotificationRepository(NotificationRepository):
    """SQLAlchemy implementation of notification repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        from database.models import Notification as NotificationModel

        db_notification = NotificationModel(
            user_id=notification.user_id,
            type=notification.type,
            title=notification.title,
            body=notification.body,
            data=notification.data,
            status=notification.status,
        )
        self._session.add(db_notification)
        await self._session.flush()
        await self._session.refresh(db_notification)

        notification.id = db_notification.id
        notification.created_at = db_notification.created_at
        return notification

    async def get_by_id(self, notification_id: int) -> Notification | None:
        """Get notification by ID."""
        from database.models import Notification as NotificationModel

        result = await self._session.execute(
            select(NotificationModel).where(NotificationModel.id == notification_id)
        )
        db_notification = result.scalar_one_or_none()

        if db_notification is None:
            return None

        return self._to_entity(db_notification)

    async def update(self, notification: Notification) -> Notification:
        """Update notification."""
        from database.models import Notification as NotificationModel

        result = await self._session.execute(
            select(NotificationModel).where(NotificationModel.id == notification.id)
        )
        db_notification = result.scalar_one()

        db_notification.status = notification.status
        db_notification.sent_at = notification.sent_at
        db_notification.read_at = notification.read_at

        await self._session.flush()
        await self._session.refresh(db_notification)

        return notification

    async def list_by_user(
        self,
        user_id: UUID,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Notification]:
        """List notifications by user."""
        from database.models import Notification as NotificationModel

        query = select(NotificationModel).where(NotificationModel.user_id == user_id)
        
        if status:
            query = query.where(NotificationModel.status == status)
        
        query = (
            query.order_by(NotificationModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self._session.execute(query)
        return [self._to_entity(n) for n in result.scalars().all()]

    async def count_unread(self, user_id: UUID) -> int:
        """Count unread notifications."""
        from database.models import Notification as NotificationModel

        result = await self._session.execute(
            select(func.count())
            .where(NotificationModel.user_id == user_id)
            .where(NotificationModel.status == "sent")
        )
        return result.scalar()

    async def get_preferences_by_user(
        self,
        user_id: UUID,
    ) -> NotificationPreference | None:
        """Get notification preferences by user."""
        from database.models import NotificationPreference as NotificationPreferenceModel

        result = await self._session.execute(
            select(NotificationPreferenceModel)
            .where(NotificationPreferenceModel.user_id == user_id)
        )
        db_pref = result.scalar_one_or_none()

        if db_pref is None:
            return None

        return self._to_preference_entity(db_pref)

    async def create_preferences(
        self,
        preferences: NotificationPreference,
    ) -> NotificationPreference:
        """Create notification preferences."""
        from database.models import NotificationPreference as NotificationPreferenceModel

        db_pref = NotificationPreferenceModel(
            user_id=preferences.user_id,
            email_enabled=preferences.email_enabled,
            sms_enabled=preferences.sms_enabled,
            push_enabled=preferences.push_enabled,
            reminder_hours=preferences.reminder_hours,
        )
        self._session.add(db_pref)
        await self._session.flush()
        await self._session.refresh(db_pref)

        preferences.id = db_pref.id
        preferences.created_at = db_pref.created_at
        preferences.updated_at = db_pref.updated_at
        return preferences

    async def update_preferences(
        self,
        preferences: NotificationPreference,
    ) -> NotificationPreference:
        """Update notification preferences."""
        from database.models import NotificationPreference as NotificationPreferenceModel

        result = await self._session.execute(
            select(NotificationPreferenceModel)
            .where(NotificationPreferenceModel.id == preferences.id)
        )
        db_pref = result.scalar_one()

        db_pref.email_enabled = preferences.email_enabled
        db_pref.sms_enabled = preferences.sms_enabled
        db_pref.push_enabled = preferences.push_enabled
        db_pref.reminder_hours = preferences.reminder_hours

        await self._session.flush()
        await self._session.refresh(db_pref)

        preferences.updated_at = db_pref.updated_at
        return preferences

    def _to_entity(self, db_notification) -> Notification:
        """Convert database model to domain entity."""
        return Notification(
            id=db_notification.id,
            user_id=db_notification.user_id,
            type=db_notification.type,
            title=db_notification.title,
            body=db_notification.body,
            data=db_notification.data or {},
            status=db_notification.status,
            sent_at=db_notification.sent_at,
            read_at=db_notification.read_at,
            created_at=db_notification.created_at,
        )

    def _to_preference_entity(
        self,
        db_pref,
    ) -> NotificationPreference:
        """Convert database model to preference entity."""
        return NotificationPreference(
            id=db_pref.id,
            user_id=db_pref.user_id,
            email_enabled=db_pref.email_enabled,
            sms_enabled=db_pref.sms_enabled,
            push_enabled=db_pref.push_enabled,
            reminder_hours=db_pref.reminder_hours,
            created_at=db_pref.created_at,
            updated_at=db_pref.updated_at,
        )
