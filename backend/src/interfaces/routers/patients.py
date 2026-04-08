"""Patient routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services import PatientService, CreatePatientInput, UpdatePatientInput
from application.interfaces.repositories import PatientRepository
from domain.exceptions import (
    PatientAlreadyExistsError,
    PatientNotFoundError,
    InvalidCPFError,
)
from infrastructure.database.connection import get_db_context
from infrastructure.repositories import SQLAlchemyPatientRepository
from interfaces.schemas import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientListResponse,
    AddAllergyRequest,
    RemoveAllergyRequest,
    UpdateMedicalHistoryRequest,
    ApiResponse,
)

router = APIRouter(prefix="/patients", tags=["patients"])


async def get_patient_service() -> PatientService:
    """Get patient service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyPatientRepository(session)
        yield PatientService(repository)


@router.post(
    "",
    response_model=ApiResponse[PatientResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create patient",
    description="Create a new patient record.",
)
async def create_patient(
    data: PatientCreate,
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Create a new patient."""
    try:
        input_data = CreatePatientInput(
            user_id=data.user_id,
            full_name=data.full_name,
            cpf=data.cpf,
            email=data.email,
            birth_date=data.birth_date,
            gender=data.gender,
            phone=data.phone,
            address=data.address,
        )
        patient = await service.create_patient(input_data)
        return ApiResponse(data=PatientResponse(**patient.to_dict()))
    except PatientAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except InvalidCPFError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=ApiResponse[PatientResponse],
    summary="Get current patient",
    description="Get the patient record for the authenticated user.",
)
async def get_current_patient(
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Get current patient."""
    try:
        patient = await service.get_patient_by_user(user_id)
        return ApiResponse(data=PatientResponse(**patient.to_dict()))
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{patient_id}",
    response_model=ApiResponse[PatientResponse],
    summary="Get patient by ID",
    description="Get a patient by their ID.",
)
async def get_patient(
    patient_id: int,
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Get patient by ID."""
    try:
        patient = await service.get_patient(patient_id)
        return ApiResponse(data=PatientResponse(**patient.to_dict()))
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/me",
    response_model=ApiResponse[PatientResponse],
    summary="Update current patient",
    description="Update the patient record for the authenticated user.",
)
async def update_current_patient(
    data: PatientUpdate,
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Update current patient."""
    try:
        patient = await service.get_patient_by_user(user_id)
        input_data = UpdatePatientInput(
            full_name=data.full_name,
            phone=data.phone,
            address=data.address,
            emergency_contact=data.emergency_contact,
        )
        updated = await service.update_patient(patient.id, input_data)
        return ApiResponse(data=PatientResponse(**updated.to_dict()))
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/me/allergies",
    response_model=ApiResponse[PatientResponse],
    summary="Add allergy",
    description="Add an allergy to the current patient.",
)
async def add_allergy(
    data: AddAllergyRequest,
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Add allergy to current patient."""
    try:
        patient = await service.get_patient_by_user(user_id)
        updated = await service.add_allergy(patient.id, data.allergy)
        return ApiResponse(data=PatientResponse(**updated.to_dict()))
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/me/allergies",
    response_model=ApiResponse[PatientResponse],
    summary="Remove allergy",
    description="Remove an allergy from the current patient.",
)
async def remove_allergy(
    data: RemoveAllergyRequest,
    user_id: UUID,  # TODO: Get from JWT token
    service: Annotated[PatientService, Depends(get_patient_service)],
) -> ApiResponse[PatientResponse]:
    """Remove allergy from current patient."""
    try:
        patient = await service.get_patient_by_user(user_id)
        updated = await service.remove_allergy(patient.id, data.allergy)
        return ApiResponse(data=PatientResponse(**updated.to_dict()))
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "",
    response_model=ApiResponse[PatientListResponse],
    summary="List patients",
    description="List all patients with optional filters.",
)
async def list_patients(
    service: Annotated[PatientService, Depends(get_patient_service)],
    limit: int = 100,
    offset: int = 0,
    name: str | None = None,
) -> ApiResponse[PatientListResponse]:
    """List patients."""
    filters = {}
    if name:
        filters["name"] = name

    patients = await service.list_patients(filters, limit, offset)
    return ApiResponse(
        data=PatientListResponse(
            patients=[PatientResponse(**p.to_dict()) for p in patients],
            total=len(patients),
        )
    )
