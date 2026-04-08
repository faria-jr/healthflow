"""Appointment routes."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import (
    AppointmentService,
    ScheduleAppointmentInput,
    UpdateAppointmentStatusInput,
)
from application.interfaces.repositories import (
    AppointmentRepository,
    PatientRepository,
    DoctorRepository,
)
from domain.exceptions import (
    AppointmentNotFoundError,
    AppointmentConflictError,
    AppointmentStatusError,
)
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import (
    SQLAlchemyAppointmentRepository,
    SQLAlchemyPatientRepository,
    SQLAlchemyDoctorRepository,
)
from interfaces.schemas import (
    AppointmentCreate,
    AppointmentUpdateStatus,
    AppointmentResponse,
    AppointmentListResponse,
    AppointmentFilterRequest,
    AddNotesRequest,
    ApiResponse,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


async def get_appointment_service() -> AppointmentService:
    """Get appointment service with repositories."""
    async with get_db_context() as session:
        appointment_repo = SQLAlchemyAppointmentRepository(session)
        patient_repo = SQLAlchemyPatientRepository(session)
        doctor_repo = SQLAlchemyDoctorRepository(session)
        yield AppointmentService(appointment_repo, patient_repo, doctor_repo)


@router.post(
    "",
    response_model=ApiResponse[AppointmentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Schedule appointment",
    description="Schedule a new appointment.",
)
async def schedule_appointment(
    data: AppointmentCreate,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Schedule a new appointment."""
    try:
        input_data = ScheduleAppointmentInput(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            scheduled_at=data.scheduled_at,
            duration_minutes=data.duration_minutes,
            notes=data.notes,
        )
        appointment = await service.schedule_appointment(input_data)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "/{appointment_id}",
    response_model=ApiResponse[AppointmentResponse],
    summary="Get appointment",
    description="Get an appointment by ID.",
)
async def get_appointment(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Get appointment by ID."""
    try:
        appointment = await service.get_appointment(appointment_id)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/{appointment_id}/status",
    response_model=ApiResponse[AppointmentResponse],
    summary="Update appointment status",
    description="Update the status of an appointment.",
)
async def update_appointment_status(
    appointment_id: int,
    data: AppointmentUpdateStatus,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Update appointment status."""
    try:
        input_data = UpdateAppointmentStatusInput(
            status=data.status,
            reason=data.reason,
        )
        appointment = await service.update_status(appointment_id, input_data)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AppointmentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post(
    "/{appointment_id}/confirm",
    response_model=ApiResponse[AppointmentResponse],
    summary="Confirm appointment",
    description="Confirm a scheduled appointment.",
)
async def confirm_appointment(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Confirm appointment."""
    try:
        appointment = await service.confirm_appointment(appointment_id)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AppointmentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post(
    "/{appointment_id}/complete",
    response_model=ApiResponse[AppointmentResponse],
    summary="Complete appointment",
    description="Mark an appointment as completed.",
)
async def complete_appointment(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Complete appointment."""
    try:
        appointment = await service.complete_appointment(appointment_id)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AppointmentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post(
    "/{appointment_id}/cancel",
    response_model=ApiResponse[AppointmentResponse],
    summary="Cancel appointment",
    description="Cancel an appointment.",
)
async def cancel_appointment(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
    reason: str | None = None,
) -> ApiResponse[AppointmentResponse]:
    """Cancel appointment."""
    try:
        appointment = await service.cancel_appointment(appointment_id, reason)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AppointmentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post(
    "/{appointment_id}/notes",
    response_model=ApiResponse[AppointmentResponse],
    summary="Add notes",
    description="Add notes to an appointment.",
)
async def add_notes(
    appointment_id: int,
    data: AddNotesRequest,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> ApiResponse[AppointmentResponse]:
    """Add notes to appointment."""
    try:
        appointment = await service.add_notes(appointment_id, data.notes)
        return ApiResponse(data=AppointmentResponse(**appointment.to_dict()))
    except AppointmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/patient/{patient_id}",
    response_model=ApiResponse[AppointmentListResponse],
    summary="List patient appointments",
    description="List appointments for a patient.",
)
async def list_patient_appointments(
    patient_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
    filters: AppointmentFilterRequest = Depends(),
) -> ApiResponse[AppointmentListResponse]:
    """List appointments for a patient."""
    appointments = await service.list_patient_appointments(
        patient_id=patient_id,
        status=filters.status,
        from_date=filters.from_date,
        limit=filters.limit,
        offset=filters.offset,
    )
    return ApiResponse(
        data=AppointmentListResponse(
            appointments=[AppointmentResponse(**a.to_dict()) for a in appointments],
            total=len(appointments),
        )
    )


@router.get(
    "/doctor/{doctor_id}",
    response_model=ApiResponse[AppointmentListResponse],
    summary="List doctor appointments",
    description="List appointments for a doctor.",
)
async def list_doctor_appointments(
    doctor_id: int,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
    filters: AppointmentFilterRequest = Depends(),
) -> ApiResponse[AppointmentListResponse]:
    """List appointments for a doctor."""
    appointments = await service.list_doctor_appointments(
        doctor_id=doctor_id,
        status=filters.status,
        from_date=filters.from_date,
        to_date=filters.to_date,
        limit=filters.limit,
        offset=filters.offset,
    )
    return ApiResponse(
        data=AppointmentListResponse(
            appointments=[AppointmentResponse(**a.to_dict()) for a in appointments],
            total=len(appointments),
        )
    )
