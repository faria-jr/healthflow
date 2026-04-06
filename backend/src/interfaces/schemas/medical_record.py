"""Medical record schemas."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MedicalRecordBase(BaseModel):
    """Base medical record schema."""

    model_config = ConfigDict(from_attributes=True)

    appointment_id: int
    diagnosis: str | None = Field(None, max_length=2000)
    symptoms: str | None = Field(None, max_length=2000)
    prescription: str | None = Field(None, max_length=2000)
    notes: str | None = Field(None, max_length=5000)


class MedicalRecordCreate(MedicalRecordBase):
    """Medical record creation schema."""

    pass


class MedicalRecordUpdate(BaseModel):
    """Medical record update schema."""

    model_config = ConfigDict(from_attributes=True)

    diagnosis: str | None = Field(None, max_length=2000)
    symptoms: str | None = Field(None, max_length=2000)
    prescription: str | None = Field(None, max_length=2000)
    notes: str | None = Field(None, max_length=5000)


class AttachmentSchema(BaseModel):
    """Attachment schema."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    url: str
    type: str
    size: int | None = None


class MedicalRecordResponse(BaseModel):
    """Medical record response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str | None
    symptoms: str | None
    prescription: str | None
    notes: str | None
    attachments: list[AttachmentSchema]
    created_at: str
    updated_at: str


class MedicalRecordListResponse(BaseModel):
    """Medical record list response."""

    records: list[MedicalRecordResponse]
    total: int


class AddAttachmentRequest(BaseModel):
    """Add attachment request."""

    name: str = Field(..., min_length=1, max_length=200)
    url: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1, max_length=100)
    size: int | None = Field(None, ge=0)


class RemoveAttachmentRequest(BaseModel):
    """Remove attachment request."""

    name: str = Field(..., min_length=1, max_length=200)
