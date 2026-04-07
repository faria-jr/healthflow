"""Notification service."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities import Notification, NotificationPreference
from domain.exceptions import NotificationNotFoundError, ValidationError
from application.interfaces.repositories import NotificationRepository


@dataclass
class CreateNotificationInput:
    """Input for creating a notification."""
    user_id: UUID
    type: str  # email, sms, push
    title: str
    body: str
    data: dict[str, Any] | None = None


@dataclass
class UpdatePreferenceInput:
    """Input for updating notification preferences."""
    email_enabled: bool | None = None
    sms_enabled: bool | None = None
    push_enabled: bool | None = None
    reminder_hours: int | None = None


class NotificationService:
    """Notification service."""

    def __init__(self, repository: NotificationRepository):
        self._repository = repository

    async def create_notification(
        self,
        input_data: CreateNotificationInput,
    ) -> Notification:
        """Create a new notification."""
        notification = Notification(
            user_id=input_data.user_id,
            type=input_data.type,
            title=input_data.title,
            body=input_data.body,
            data=input_data.data or {},
        )
        return await self._repository.create(notification)

    async def get_notification(self, notification_id: int) -> Notification:
        """Get notification by ID."""
        notification = await self._repository.get_by_id(notification_id)
        if not notification:
            raise NotificationNotFoundError(
                f"Notification with ID {notification_id} not found"
            )
        return notification

    async def mark_as_sent(self, notification_id: int) -> Notification:
        """Mark notification as sent."""
        notification = await self.get_notification(notification_id)
        notification.mark_as_sent()
        return await self._repository.update(notification)

    async def mark_as_read(self, notification_id: int) -> Notification:
        """Mark notification as read."""
        notification = await self.get_notification(notification_id)
        notification.mark_as_read()
        return await self._repository.update(notification)

    async def list_user_notifications(
        self,
        user_id: UUID,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Notification]:
        """List notifications for a user."""
        return await self._repository.list_by_user(user_id, status, limit, offset)

    async def get_unread_count(self, user_id: UUID) -> int:
        """Get count of unread notifications."""
        return await self._repository.count_unread(user_id)

    async def get_or_create_preferences(
        self,
        user_id: UUID,
    ) -> NotificationPreference:
        """Get or create notification preferences."""
        preferences = await self._repository.get_preferences_by_user(user_id)
        if not preferences:
            preferences = NotificationPreference(user_id=user_id)
            preferences = await self._repository.create_preferences(preferences)
        return preferences

    async def update_preferences(
        self,
        user_id: UUID,
        input_data: UpdatePreferenceInput,
    ) -> NotificationPreference:
        """Update notification preferences."""
        preferences = await self.get_or_create_preferences(user_id)
        preferences.update_preferences(
            email=input_data.email_enabled,
            sms=input_data.sms_enabled,
            push=input_data.push_enabled,
            reminder_hours=input_data.reminder_hours,
        )
        return await self._repository.update_preferences(preferences)
