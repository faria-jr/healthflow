"""Application services."""

from .patient_service import PatientService, CreatePatientInput, UpdatePatientInput
from .doctor_service import DoctorService, CreateDoctorInput, UpdateDoctorInput
from .appointment_service import (
    AppointmentService,
    ScheduleAppointmentInput,
    UpdateAppointmentStatusInput,
)
from .medical_record_service import (
    MedicalRecordService,
    CreateMedicalRecordInput,
    UpdateMedicalRecordInput,
)

__all__ = [
    "PatientService",
    "CreatePatientInput",
    "UpdatePatientInput",
    "DoctorService",
    "CreateDoctorInput",
    "UpdateDoctorInput",
    "AppointmentService",
    "ScheduleAppointmentInput",
    "UpdateAppointmentStatusInput",
    "MedicalRecordService",
    "CreateMedicalRecordInput",
    "UpdateMedicalRecordInput",
]
