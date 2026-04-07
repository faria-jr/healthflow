"""Lab result service."""

from dataclasses import dataclass

from domain.entities import LabResult
from domain.exceptions import LabResultNotFoundError, ValidationError
from application.interfaces.repositories import LabResultRepository


@dataclass
class CreateLabResultInput:
    """Input for creating a lab result."""
    patient_id: int
    lab_name: str
    test_type: str
    doctor_id: int | None = None
    appointment_id: int | None = None
    result_summary: str | None = None


@dataclass
class AttachFileInput:
    """Input for attaching a file."""
    file_url: str
    file_name: str
    file_size: int


class LabResultService:
    """Lab result service."""

    def __init__(self, repository: LabResultRepository):
        self._repository = repository

    async def create_lab_result(
        self,
        input_data: CreateLabResultInput,
    ) -> LabResult:
        """Create a new lab result."""
        lab_result = LabResult(
            patient_id=input_data.patient_id,
            lab_name=input_data.lab_name,
            test_type=input_data.test_type,
            doctor_id=input_data.doctor_id,
            appointment_id=input_data.appointment_id,
            result_summary=input_data.result_summary,
        )
        return await self._repository.create(lab_result)

    async def get_lab_result(self, lab_result_id: int) -> LabResult:
        """Get lab result by ID."""
        lab_result = await self._repository.get_by_id(lab_result_id)
        if not lab_result:
            raise LabResultNotFoundError(
                f"Lab result with ID {lab_result_id} not found"
            )
        return lab_result

    async def attach_file(
        self,
        lab_result_id: int,
        input_data: AttachFileInput,
    ) -> LabResult:
        """Attach file to lab result."""
        lab_result = await self.get_lab_result(lab_result_id)
        lab_result.attach_file(
            input_data.file_url,
            input_data.file_name,
            input_data.file_size,
        )
        return await self._repository.update(lab_result)

    async def mark_as_processing(self, lab_result_id: int) -> LabResult:
        """Mark lab result as processing."""
        lab_result = await self.get_lab_result(lab_result_id)
        lab_result.mark_as_processing()
        return await self._repository.update(lab_result)

    async def mark_as_completed(self, lab_result_id: int) -> LabResult:
        """Mark lab result as completed."""
        lab_result = await self.get_lab_result(lab_result_id)
        lab_result.mark_as_completed()
        return await self._repository.update(lab_result)

    async def list_patient_lab_results(
        self,
        patient_id: int,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[LabResult]:
        """List lab results for a patient."""
        return await self._repository.list_by_patient(
            patient_id, status, limit, offset
        )

    async def list_doctor_lab_results(
        self,
        doctor_id: int,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[LabResult]:
        """List lab results for a doctor."""
        return await self._repository.list_by_doctor(
            doctor_id, status, limit, offset
        )
