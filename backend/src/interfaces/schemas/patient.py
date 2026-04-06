"""Patient schemas."""

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PatientBase(BaseModel):
    """Base patient schema."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=3, max_length=200)
    cpf: str = Field(..., min_length=11, max_length=14)
    phone: str | None = Field(None, max_length=20)
    email: EmailStr
    birth_date: date
    gender: str = Field(..., pattern="^(male|female|other|prefer_not_to_say)$")
    address: str | None = Field(None, max_length=500)


class PatientCreate(PatientBase):
    """Patient creation schema."""

    user_id: UUID
    emergency_contact: dict[str, Any] | None = None
    medical_history: dict[str, Any] = Field(default_factory=dict)
    allergies: list[str] = Field(default_factory=list)


class PatientUpdate(BaseModel):
    """Patient update schema."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str | None = Field(None, min_length=3, max_length=200)
    phone: str | None = Field(None, max_length=20)
    address: str | None = Field(None, max_length=500)
    emergency_contact: dict[str, Any] | None = None


class PatientResponse(PatientBase):
    """Patient response schema."""

    id: int
    user_id: UUID
    emergency_contact: dict[str, Any] | None = None
    medical_history: dict[str, Any]
    allergies: list[str]
    created_at: str
    updated_at: str


class PatientListResponse(BaseModel):
    """Patient list response."""

    patients: list[PatientResponse]
    total: int


class AddAllergyRequest(BaseModel):
    """Add allergy request."""

    allergy: str = Field(..., min_length=1, max_length=200)


class RemoveAllergyRequest(BaseModel):
    """Remove allergy request."""

    allergy: str = Field(..., min_length=1, max_length=200)


class UpdateMedicalHistoryRequest(BaseModel):
    """Update medical history request."""

    data: dict[str, Any]
