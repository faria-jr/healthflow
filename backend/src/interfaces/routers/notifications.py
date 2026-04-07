"""Notification routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.notification_service import NotificationService
from domain.exceptions import NotificationNotFoundError, ValidationError
from infrastructure.database.connection import get_db_context
from infrastructure.repositories.notification_repository import SQLAlchemyNotificationRepository
from interfaces.schemas.common import ApiResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


async def get_notification_service():
    """Get notification service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyNotificationRepository(session)
        yield NotificationService(repository)


@router.get(
    "",
    response_model=ApiResponse,
    summary="List user notifications",
)
async def list_notifications(
    user_id: UUID,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: Annotated[NotificationService, Depends(get_notification_service)] = None,
):
    """List notifications for a user."""
    notifications = await service.list_user_notifications(user_id, status, limit, offset)
    return ApiResponse(data={"notifications": [n.to_dict() for n in notifications]})


@router.get(
    "/unread-count",
    response_model=ApiResponse,
    summary="Get unread notification count",
)
async def get_unread_count(
    user_id: UUID,
    service: Annotated[NotificationService, Depends(get_notification_service)] = None,
):
    """Get count of unread notifications."""
    count = await service.get_unread_count(user_id)
    return ApiResponse(data={"count": count})


@router.post(
    "/{notification_id}/read",
    response_model=ApiResponse,
    summary="Mark notification as read",
)
async def mark_notification_read(
    notification_id: int,
    service: Annotated[NotificationService, Depends(get_notification_service)] = None,
):
    """Mark notification as read."""
    try:
        notification = await service.mark_as_read(notification_id)
        return ApiResponse(data=notification.to_dict())
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/preferences",
    response_model=ApiResponse,
    summary="Get notification preferences",
)
async def get_preferences(
    user_id: UUID,
    service: Annotated[NotificationService, Depends(get_notification_service)] = None,
):
    """Get notification preferences."""
    preferences = await service.get_or_create_preferences(user_id)
    return ApiResponse(data=preferences.to_dict())


@router.put(
    "/preferences",
    response_model=ApiResponse,
    summary="Update notification preferences",
)
async def update_preferences(
    user_id: UUID,
    email_enabled: bool | None = None,
    sms_enabled: bool | None = None,
    push_enabled: bool | None = None,
    reminder_hours: int | None = None,
    service: Annotated[NotificationService, Depends(get_notification_service)] = None,
):
    """Update notification preferences."""
    from application.services.notification_service import UpdatePreferenceInput
    
    try:
        input_data = UpdatePreferenceInput(
            email_enabled=email_enabled,
            sms_enabled=sms_enabled,
            push_enabled=push_enabled,
            reminder_hours=reminder_hours,
        )
        preferences = await service.update_preferences(user_id, input_data)
        return ApiResponse(data=preferences.to_dict())
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
