"""Lab result routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.lab_result_service import LabResultService
from domain.exceptions import LabResultNotFoundError, ValidationError
from infrastructure.database.connection import get_db_context
from infrastructure.repositories.lab_result_repository import SQLAlchemyLabResultRepository
from interfaces.schemas.common import ApiResponse

router = APIRouter(prefix="/lab-results", tags=["lab-results"])


async def get_lab_result_service():
    """Get lab result service with repository."""
    async with get_db_context() as session:
        repository = SQLAlchemyLabResultRepository(session)
        yield LabResultService(repository)


@router.post(
    "",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create lab result",
)
async def create_lab_result(
    patient_id: int,
    lab_name: str,
    test_type: str,
    doctor_id: int | None = None,
    appointment_id: int | None = None,
    result_summary: str | None = None,
    service: Annotated[LabResultService, Depends(get_lab_result_service)] = None,
):
    """Create a new lab result."""
    from application.services.lab_result_service import CreateLabResultInput
    
    try:
        input_data = CreateLabResultInput(
            patient_id=patient_id,
            lab_name=lab_name,
            test_type=test_type,
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            result_summary=result_summary,
        )
        lab_result = await service.create_lab_result(input_data)
        return ApiResponse(data=lab_result.to_dict())
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get(
    "/{lab_result_id}",
    response_model=ApiResponse,
    summary="Get lab result by ID",
)
async def get_lab_result(
    lab_result_id: int,
    service: Annotated[LabResultService, Depends(get_lab_result_service)] = None,
):
    """Get lab result by ID."""
    try:
        lab_result = await service.get_lab_result(lab_result_id)
        return ApiResponse(data=lab_result.to_dict())
    except LabResultNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/patient/{patient_id}",
    response_model=ApiResponse,
    summary="List patient lab results",
)
async def list_patient_lab_results(
    patient_id: int,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: Annotated[LabResultService, Depends(get_lab_result_service)] = None,
):
    """List lab results for a patient."""
    lab_results = await service.list_patient_lab_results(patient_id, status, limit, offset)
    return ApiResponse(data={"lab_results": [r.to_dict() for r in lab_results]})


@router.get(
    "/doctor/{doctor_id}",
    response_model=ApiResponse,
    summary="List doctor lab results",
)
async def list_doctor_lab_results(
    doctor_id: int,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: Annotated[LabResultService, Depends(get_lab_result_service)] = None,
):
    """List lab results for a doctor."""
    lab_results = await service.list_doctor_lab_results(doctor_id, status, limit, offset)
    return ApiResponse(data={"lab_results": [r.to_dict() for r in lab_results]})


@router.post(
    "/{lab_result_id}/attach",
    response_model=ApiResponse,
    summary="Attach file to lab result",
)
async def attach_file(
    lab_result_id: int,
    file_url: str,
    file_name: str,
    file_size: int,
    service: Annotated[LabResultService, Depends(get_lab_result_service)] = None,
):
    """Attach file to lab result."""
    from application.services.lab_result_service import AttachFileInput
    
    try:
        input_data = AttachFileInput(
            file_url=file_url,
            file_name=file_name,
            file_size=file_size,
        )
        lab_result = await service.attach_file(lab_result_id, input_data)
        return ApiResponse(data=lab_result.to_dict())
    except LabResultNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
