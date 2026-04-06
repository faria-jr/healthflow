"""Schemas."""

from .common import ApiResponse, ErrorResponse, PaginatedResponse, PaginationMeta
from .patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientListResponse,
    AddAllergyRequest,
    RemoveAllergyRequest,
    UpdateMedicalHistoryRequest,
)
from .doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorListResponse,
    DoctorFilterRequest,
)
from .appointment import (
    AppointmentCreate,
    AppointmentUpdateStatus,
    AppointmentResponse,
    AppointmentListResponse,
    AppointmentFilterRequest,
    AddNotesRequest,
)
from .medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
    MedicalRecordListResponse,
    AddAttachmentRequest,
    RemoveAttachmentRequest,
)

__all__ = [
    "ApiResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "PaginationMeta",
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "PatientListResponse",
    "AddAllergyRequest",
    "RemoveAllergyRequest",
    "UpdateMedicalHistoryRequest",
    "DoctorCreate",
    "DoctorUpdate",
    "DoctorResponse",
    "DoctorListResponse",
    "DoctorFilterRequest",
    "AppointmentCreate",
    "AppointmentUpdateStatus",
    "AppointmentResponse",
    "AppointmentListResponse",
    "AppointmentFilterRequest",
    "AddNotesRequest",
    "MedicalRecordCreate",
    "MedicalRecordUpdate",
    "MedicalRecordResponse",
    "MedicalRecordListResponse",
    "AddAttachmentRequest",
    "RemoveAttachmentRequest",
]
