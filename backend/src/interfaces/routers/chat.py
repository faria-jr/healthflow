"""Chat routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import ChatService
from application.interfaces.repositories import ChatMessageRepository
from domain.exceptions import ChatMessageNotFoundError, ValidationError
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import SQLAlchemyChatMessageRepository
from interfaces.schemas import ApiResponse

router = APIRouter(prefix="/chat", tags=["chat"])


async def get_chat_service():
    """Get chat service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyChatMessageRepository(session)
        yield ChatService(repository)


@router.get(
    "/appointments/{appointment_id}/messages",
    response_model=ApiResponse,
    summary="List chat messages",
)
async def list_messages(
    appointment_id: int,
    limit: int = 100,
    offset: int = 0,
    service: Annotated[ChatService, Depends(get_chat_service)] = None,
):
    """List chat messages for an appointment."""
    messages = await service.list_appointment_messages(appointment_id, limit, offset)
    return ApiResponse(data={"messages": [m.to_dict() for m in messages]})


@router.get(
    "/appointments/{appointment_id}/unread-count",
    response_model=ApiResponse,
    summary="Get unread message count",
)
async def get_unread_count(
    appointment_id: int,
    user_id: UUID,
    service: Annotated[ChatService, Depends(get_chat_service)] = None,
):
    """Get count of unread messages."""
    count = await service.get_unread_count(appointment_id, user_id)
    return ApiResponse(data={"count": count})


@router.post(
    "/messages/{message_id}/read",
    response_model=ApiResponse,
    summary="Mark message as read",
)
async def mark_message_read(
    message_id: int,
    service: Annotated[ChatService, Depends(get_chat_service)] = None,
):
    """Mark message as read."""
    try:
        message = await service.mark_as_read(message_id)
        return ApiResponse(data=message.to_dict())
    except ChatMessageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
