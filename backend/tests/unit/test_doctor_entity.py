"""Tests for Doctor entity."""

from decimal import Decimal
from uuid import uuid4

import pytest

from domain.entities import Doctor, validate_crm, format_crm
from domain.exceptions import InvalidCRMError


class TestCRMValidation:
    """Test CRM validation functions."""

    def test_validate_crm_valid(self):
        """Test valid CRM validation."""
        assert validate_crm("CRM/SP 123456") is True
        assert validate_crm("CRM/RJ 12345") is True
        assert validate_crm("CRM123456SP") is True

    def test_validate_crm_invalid(self):
        """Test invalid CRM validation."""
        assert validate_crm("CRM/XX 123456") is False  # Invalid state
        assert validate_crm("invalid") is False
        assert validate_crm("123") is False

    def test_format_crm(self):
        """Test CRM formatting."""
        assert format_crm("CRM/SP 123456") == "CRM/SP 123456"
        assert format_crm("CRM123456SP") == "CRM/SP 123456"


class TestDoctorEntity:
    """Test Doctor entity."""

    def test_create_doctor_success(self):
        """Test successful doctor creation."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
        )
        
        assert doctor.full_name == "Dr. Maria Santos"
        assert doctor.crm == "CRM/SP 123456"
        assert doctor.specialty == "Cardiologia"
        assert doctor.is_active is True

    def test_create_doctor_invalid_crm(self):
        """Test doctor creation with invalid CRM."""
        with pytest.raises(InvalidCRMError):
            Doctor(
                user_id=uuid4(),
                full_name="Dr. Maria Santos",
                crm="CRM/XX 123456",  # Invalid state
                specialty="Cardiologia",
                email="maria.santos@example.com",
            )

    def test_create_doctor_invalid_name(self):
        """Test doctor creation with invalid name."""
        with pytest.raises(InvalidCRMError):
            Doctor(
                user_id=uuid4(),
                full_name="Dr",
                crm="CRM/SP 123456",
                specialty="Cardiologia",
                email="maria.santos@example.com",
            )

    def test_create_doctor_invalid_specialty(self):
        """Test doctor creation with invalid specialty."""
        with pytest.raises(InvalidCRMError):
            Doctor(
                user_id=uuid4(),
                full_name="Dr. Maria Santos",
                crm="CRM/SP 123456",
                specialty="A",  # Too short
                email="maria.santos@example.com",
            )

    def test_create_doctor_negative_fee(self):
        """Test doctor creation with negative consultation fee."""
        with pytest.raises(InvalidCRMError):
            Doctor(
                user_id=uuid4(),
                full_name="Dr. Maria Santos",
                crm="CRM/SP 123456",
                specialty="Cardiologia",
                email="maria.santos@example.com",
                consultation_fee=Decimal("-100.00"),
            )

    def test_deactivate_doctor(self):
        """Test deactivating doctor."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
        )
        
        doctor.deactivate()
        assert doctor.is_active is False

    def test_activate_doctor(self):
        """Test activating doctor."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
        )
        
        doctor.deactivate()
        doctor.activate()
        assert doctor.is_active is True

    def test_update_fee(self):
        """Test updating consultation fee."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
            consultation_fee=Decimal("200.00"),
        )
        
        doctor.update_fee(Decimal("250.00"))
        assert doctor.consultation_fee == Decimal("250.00")

    def test_update_fee_negative(self):
        """Test updating fee with negative value."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
        )
        
        with pytest.raises(InvalidCRMError):
            doctor.update_fee(Decimal("-100.00"))

    def test_to_dict(self):
        """Test doctor to dict conversion."""
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria.santos@example.com",
            consultation_fee=Decimal("250.00"),
        )
        
        data = doctor.to_dict()
        assert data["full_name"] == "Dr. Maria Santos"
        assert data["crm"] == "CRM/SP 123456"
        assert data["specialty"] == "Cardiologia"
        assert data["is_active"] is True
        assert data["consultation_fee"] == "250.00"
