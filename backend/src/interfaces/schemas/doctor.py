"""Doctor schemas."""

from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class DoctorBase(BaseModel):
    """Base doctor schema."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=3, max_length=200)
    crm: str = Field(..., min_length=6, max_length=20)
    specialty: str = Field(..., min_length=2, max_length=100)
    phone: str | None = Field(None, max_length=20)
    email: EmailStr
    bio: str | None = Field(None, max_length=2000)
    consultation_fee: Decimal | None = Field(None, ge=0)


class DoctorCreate(DoctorBase):
    """Doctor creation schema."""

    user_id: UUID


class DoctorUpdate(BaseModel):
    """Doctor update schema."""

    model_config = ConfigDict(from_attributes=True)

    full_name: str | None = Field(None, min_length=3, max_length=200)
    specialty: str | None = Field(None, min_length=2, max_length=100)
    phone: str | None = Field(None, max_length=20)
    bio: str | None = Field(None, max_length=2000)
    consultation_fee: Decimal | None = Field(None, ge=0)
    is_active: bool | None = None


class DoctorResponse(DoctorBase):
    """Doctor response schema."""

    id: int
    user_id: UUID
    is_active: bool
    created_at: str
    updated_at: str


class DoctorListResponse(BaseModel):
    """Doctor list response."""

    doctors: list[DoctorResponse]
    total: int


class DoctorFilterRequest(BaseModel):
    """Doctor filter request."""

    specialty: str | None = None
    name: str | None = None
    is_active: bool | None = True
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)
