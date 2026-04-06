"""Tests for Patient entity."""

from datetime import date
from uuid import uuid4

import pytest

from domain.entities import Patient, validate_cpf, format_cpf
from domain.exceptions import InvalidCPFError


class TestCPFValidation:
    """Test CPF validation functions."""

    def test_validate_cpf_valid(self):
        """Test valid CPF validation."""
        assert validate_cpf("529.982.247-25") is True
        assert validate_cpf("52998224725") is True

    def test_validate_cpf_invalid(self):
        """Test invalid CPF validation."""
        assert validate_cpf("111.111.111-11") is False
        assert validate_cpf("000.000.000-00") is False
        assert validate_cpf("123.456.789-00") is False
        assert validate_cpf("invalid") is False
        assert validate_cpf("123") is False

    def test_format_cpf(self):
        """Test CPF formatting."""
        assert format_cpf("52998224725") == "529.982.247-25"
        assert format_cpf("529.982.247-25") == "529.982.247-25"


class TestPatientEntity:
    """Test Patient entity."""

    def test_create_patient_success(self):
        """Test successful patient creation."""
        patient = Patient(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao.silva@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        
        assert patient.full_name == "João Silva"
        assert patient.cpf == "529.982.247-25"
        assert patient.email == "joao.silva@example.com"
        assert patient.allergies == []
        assert patient.medical_history == {}

    def test_create_patient_invalid_cpf(self):
        """Test patient creation with invalid CPF."""
        with pytest.raises(InvalidCPFError):
            Patient(
                user_id=uuid4(),
                full_name="João Silva",
                cpf="111.111.111-11",
                email="joao.silva@example.com",
                birth_date=date(1990, 5, 15),
                gender="male",
            )

    def test_create_patient_invalid_name(self):
        """Test patient creation with invalid name."""
        with pytest.raises(InvalidCPFError):
            Patient(
                user_id=uuid4(),
                full_name="Jo",
                cpf="529.982.247-25",
                email="joao.silva@example.com",
                birth_date=date(1990, 5, 15),
                gender="male",
            )

    def test_create_patient_invalid_gender(self):
        """Test patient creation with invalid gender."""
        with pytest.raises(InvalidCPFError):
            Patient(
                user_id=uuid4(),
                full_name="João Silva",
                cpf="529.982.247-25",
                email="joao.silva@example.com",
                birth_date=date(1990, 5, 15),
                gender="invalid_gender",
            )

    def test_add_allergy(self):
        """Test adding allergy."""
        patient = Patient(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao.silva@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        
        patient.add_allergy("Penicilina")
        assert "Penicilina" in patient.allergies
        
        # Duplicate should not be added
        patient.add_allergy("Penicilina")
        assert patient.allergies.count("Penicilina") == 1

    def test_remove_allergy(self):
        """Test removing allergy."""
        patient = Patient(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao.silva@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        
        patient.add_allergy("Penicilina")
        patient.remove_allergy("Penicilina")
        assert "Penicilina" not in patient.allergies
        
        # Removing non-existent should not error
        patient.remove_allergy("NonExistent")

    def test_update_medical_history(self):
        """Test updating medical history."""
        patient = Patient(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao.silva@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        
        patient.update_medical_history({"surgery": "Appendectomy"})
        assert patient.medical_history["surgery"] == "Appendectomy"
        
        patient.update_medical_history({"condition": "Hypertension"})
        assert patient.medical_history["condition"] == "Hypertension"
        assert patient.medical_history["surgery"] == "Appendectomy"

    def test_to_dict(self):
        """Test patient to dict conversion."""
        patient = Patient(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao.silva@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
            phone="(11) 98765-4321",
        )
        
        data = patient.to_dict()
        assert data["full_name"] == "João Silva"
        assert data["cpf"] == "529.982.247-25"
        assert data["gender"] == "male"
        assert "user_id" in data
