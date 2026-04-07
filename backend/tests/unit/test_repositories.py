"""Unit tests for repositories."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from domain.entities import Patient, Doctor, Appointment
from infrastructure.repositories import (
    SQLAlchemyPatientRepository,
    SQLAlchemyDoctorRepository,
    SQLAlchemyAppointmentRepository,
)


@pytest.mark.asyncio
class TestPatientRepository:
    """Test Patient repository."""

    async def test_create_patient(self, db_session):
        """Test creating a patient."""
        repo = SQLAlchemyPatientRepository(db_session)
        
        patient = Patient(
            user_id=uuid4(),
            full_name="Test Patient",
            cpf="529.982.247-25",
            email="test@example.com",
            birth_date=datetime.now().date(),
            gender="male",
        )
        
        result = await repo.create(patient)
        assert result.id is not None
        assert result.full_name == "Test Patient"

    async def test_get_patient_by_id(self, db_session):
        """Test getting patient by ID."""
        repo = SQLAlchemyPatientRepository(db_session)
        
        # Create patient
        patient = Patient(
            user_id=uuid4(),
            full_name="Test Patient",
            cpf="529.982.247-25",
            email="test@example.com",
            birth_date=datetime.now().date(),
            gender="male",
        )
        created = await repo.create(patient)
        
        # Get by ID
        result = await repo.get_by_id(created.id)
        assert result is not None
        assert result.full_name == "Test Patient"

    async def test_get_patient_by_cpf(self, db_session):
        """Test getting patient by CPF."""
        repo = SQLAlchemyPatientRepository(db_session)
        
        patient = Patient(
            user_id=uuid4(),
            full_name="Test Patient",
            cpf="529.982.247-25",
            email="test@example.com",
            birth_date=datetime.now().date(),
            gender="male",
        )
        await repo.create(patient)
        
        result = await repo.get_by_cpf("52998224725")
        assert result is not None
        assert result.full_name == "Test Patient"

    async def test_update_patient(self, db_session):
        """Test updating a patient."""
        repo = SQLAlchemyPatientRepository(db_session)
        
        patient = Patient(
            user_id=uuid4(),
            full_name="Test Patient",
            cpf="529.982.247-25",
            email="test@example.com",
            birth_date=datetime.now().date(),
            gender="male",
        )
        created = await repo.create(patient)
        
        # Update
        created.full_name = "Updated Name"
        updated = await repo.update(created)
        
        assert updated.full_name == "Updated Name"

    async def test_list_patients(self, db_session):
        """Test listing patients."""
        repo = SQLAlchemyPatientRepository(db_session)
        
        # Create multiple patients
        for i in range(3):
            patient = Patient(
                user_id=uuid4(),
                full_name=f"Patient {i}",
                cpf=f"529.982.247-{i+10}",
                email=f"patient{i}@example.com",
                birth_date=datetime.now().date(),
                gender="male",
            )
            await repo.create(patient)
        
        results = await repo.list()
        assert len(results) >= 3


@pytest.mark.asyncio
class TestDoctorRepository:
    """Test Doctor repository."""

    async def test_create_doctor(self, db_session):
        """Test creating a doctor."""
        repo = SQLAlchemyDoctorRepository(db_session)
        
        from decimal import Decimal
        
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Test",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="doctor@example.com",
            consultation_fee=Decimal("250.00"),
        )
        
        result = await repo.create(doctor)
        assert result.id is not None
        assert result.full_name == "Dr. Test"

    async def test_get_doctor_by_crm(self, db_session):
        """Test getting doctor by CRM."""
        repo = SQLAlchemyDoctorRepository(db_session)
        
        from decimal import Decimal
        
        doctor = Doctor(
            user_id=uuid4(),
            full_name="Dr. Test",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="doctor@example.com",
            consultation_fee=Decimal("250.00"),
        )
        await repo.create(doctor)
        
        result = await repo.get_by_crm("CRM/SP 123456")
        assert result is not None
        assert result.full_name == "Dr. Test"

    async def test_list_doctors_by_specialty(self, db_session):
        """Test listing doctors by specialty."""
        repo = SQLAlchemyDoctorRepository(db_session)
        
        from decimal import Decimal
        
        # Create doctors with different specialties
        for specialty in ["Cardiologia", "Dermatologia", "Cardiologia"]:
            doctor = Doctor(
                user_id=uuid4(),
                full_name=f"Dr. {specialty}",
                crm=f"CRM/SP {hash(specialty) % 100000}",
                specialty=specialty,
                email=f"{specialty.lower()}@example.com",
                consultation_fee=Decimal("250.00"),
            )
            await repo.create(doctor)
        
        results = await repo.list_by_specialty("Cardiologia")
        assert len(results) >= 2


@pytest.mark.asyncio
class TestAppointmentRepository:
    """Test Appointment repository."""

    async def test_create_appointment(self, db_session, sample_patient_data, sample_doctor_data):
        """Test creating an appointment."""
        # First create patient and doctor
        patient_repo = SQLAlchemyPatientRepository(db_session)
        doctor_repo = SQLAlchemyDoctorRepository(db_session)
        
        patient = Patient(**sample_patient_data)
        doctor = Doctor(**sample_doctor_data)
        
        created_patient = await patient_repo.create(patient)
        created_doctor = await doctor_repo.create(doctor)
        
        # Create appointment
        repo = SQLAlchemyAppointmentRepository(db_session)
        
        future_time = datetime.now() + timedelta(days=1)
        appointment = Appointment(
            patient_id=created_patient.id,
            doctor_id=created_doctor.id,
            scheduled_at=future_time,
            duration_minutes=30,
        )
        
        result = await repo.create(appointment)
        assert result.id is not None
        assert result.status == "scheduled"

    async def test_check_conflicts(self, db_session, sample_patient_data, sample_doctor_data):
        """Test checking for appointment conflicts."""
        # Setup
        patient_repo = SQLAlchemyPatientRepository(db_session)
        doctor_repo = SQLAlchemyDoctorRepository(db_session)
        
        patient = Patient(**sample_patient_data)
        doctor = Doctor(**sample_doctor_data)
        
        created_patient = await patient_repo.create(patient)
        created_doctor = await doctor_repo.create(doctor)
        
        repo = SQLAlchemyAppointmentRepository(db_session)
        
        # Create first appointment
        future_time = datetime.now() + timedelta(days=1)
        appointment1 = Appointment(
            patient_id=created_patient.id,
            doctor_id=created_doctor.id,
            scheduled_at=future_time,
            duration_minutes=30,
