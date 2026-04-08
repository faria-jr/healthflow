"""Doctor routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import DoctorService, CreateDoctorInput, UpdateDoctorInput
from application.interfaces.repositories import DoctorRepository
from domain.exceptions import (
    DoctorAlreadyExistsError,
    DoctorNotFoundError,
    InvalidCRMError,
)
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import SQLAlchemyDoctorRepository
from interfaces.schemas import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorListResponse,
    DoctorFilterRequest,
    ApiResponse,
)

router = APIRouter(prefix="/doctors", tags=["doctors"])


async def get_doctor_service() -> DoctorService:
    """Get doctor service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyDoctorRepository(session)
        yield DoctorService(repository)


@router.post(
    "",
    response_model=ApiResponse[DoctorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create doctor",
    description="Create a new doctor record.",
)
async def create_doctor(
    data: DoctorCreate,
    service: Annotated[DoctorService, Depends(get_doctor_service)],
) -> ApiResponse[DoctorResponse]:
    """Create a new doctor."""
    try:
        input_data = CreateDoctorInput(
            user_id=data.user_id,
            full_name=data.full_name,
            crm=data.crm,
            specialty=data.specialty,
            email=data.email,
            phone=data.phone,
            bio=data.bio,
            consultation_fee=data.consultation_fee,
        )
        doctor = await service.create_doctor(input_data)
        return ApiResponse(data=DoctorResponse(**doctor.to_dict()))
    except DoctorAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except InvalidCRMError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=ApiResponse[DoctorResponse],
    summary="Get current doctor",
    description="Get the doctor record for the authenticated user.",
)
async def get_current_doctor(
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[DoctorService, Depends(get_doctor_service)],
) -> ApiResponse[DoctorResponse]:
    """Get current doctor."""
    try:
        doctor = await service.get_doctor_by_user(user_id)
        return ApiResponse(data=DoctorResponse(**doctor.to_dict()))
    except DoctorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{doctor_id}",
    response_model=ApiResponse[DoctorResponse],
    summary="Get doctor by ID",
    description="Get a doctor by their ID.",
)
async def get_doctor(
    doctor_id: int,
    service: Annotated[DoctorService, Depends(get_doctor_service)],
) -> ApiResponse[DoctorResponse]:
    """Get doctor by ID."""
    try:
        doctor = await service.get_doctor(doctor_id)
        return ApiResponse(data=DoctorResponse(**doctor.to_dict()))
    except DoctorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/me",
    response_model=ApiResponse[DoctorResponse],
    summary="Update current doctor",
    description="Update the doctor record for the authenticated user.",
)
async def update_current_doctor(
    data: DoctorUpdate,
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[DoctorService, Depends(get_doctor_service)],
) -> ApiResponse[DoctorResponse]:
    """Update current doctor."""
    try:
        doctor = await service.get_doctor_by_user(user_id)
        input_data = UpdateDoctorInput(
            full_name=data.full_name,
            specialty=data.specialty,
            phone=data.phone,
            bio=data.bio,
            consultation_fee=data.consultation_fee,
            is_active=data.is_active,
        )
        updated = await service.update_doctor(doctor.id, input_data)
        return ApiResponse(data=DoctorResponse(**updated.to_dict()))
    except DoctorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "",
    response_model=ApiResponse[DoctorListResponse],
    summary="List doctors",
    description="List all doctors with optional filters.",
)
async def list_doctors(
    service: Annotated[DoctorService, Depends(get_doctor_service)],
    filters: DoctorFilterRequest = Depends(),
) -> ApiResponse[DoctorListResponse]:
    """List doctors."""
    filter_dict = {}
    if filters.specialty:
        filter_dict["specialty"] = filters.specialty
    if filters.name:
        filter_dict["name"] = filters.name
    if filters.is_active is not None:
        filter_dict["is_active"] = filters.is_active

    doctors = await service.list_doctors(
        filter_dict, filters.limit, filters.offset
    )
    return ApiResponse(
        data=DoctorListResponse(
            doctors=[DoctorResponse(**d.to_dict()) for d in doctors],
            total=len(doctors),
        )
    )


@router.get(
    "/specialty/{specialty}",
    response_model=ApiResponse[DoctorListResponse],
    summary="List doctors by specialty",
    description="List doctors filtered by specialty.",
)
async def list_doctors_by_specialty(
    specialty: str,
    service: Annotated[DoctorService, Depends(get_doctor_service)],
    limit: int = 100,
    offset: int = 0,
) -> ApiResponse[DoctorListResponse]:
    """List doctors by specialty."""
    doctors = await service.list_doctors_by_specialty(specialty, limit, offset)
    return ApiResponse(
        data=DoctorListResponse(
            doctors=[DoctorResponse(**d.to_dict()) for d in doctors],
            total=len(doctors),
        )
    )
