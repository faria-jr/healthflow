"""Unit tests for services."""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from domain.entities import Patient, Doctor, Appointment
from domain.exceptions import (
    PatientAlreadyExistsError,
    DoctorAlreadyExistsError,
    AppointmentConflictError,
)
from application.services import (
    PatientService,
    DoctorService,
    AppointmentService,
)


class MockPatientRepository:
    """Mock patient repository for testing."""
    
    def __init__(self):
        self.patients = {}
        self.next_id = 1
    
    async def create(self, patient):
        patient.id = self.next_id
        self.patients[self.next_id] = patient
        self.next_id += 1
        return patient
    
    async def get_by_id(self, patient_id):
        return self.patients.get(patient_id)
    
    async def get_by_user_id(self, user_id):
        for p in self.patients.values():
            if p.user_id == user_id:
                return p
        return None
    
    async def get_by_cpf(self, cpf):
        for p in self.patients.values():
            if p.cpf == cpf:
                return p
        return None
    
    async def get_by_email(self, email):
        for p in self.patients.values():
            if p.email == email:
                return p
        return None
    
    async def update(self, patient):
        self.patients[patient.id] = patient
        return patient
    
    async def list(self, filters=None, limit=100, offset=0):
        return list(self.patients.values())


class MockDoctorRepository:
    """Mock doctor repository for testing."""
    
    def __init__(self):
        self.doctors = {}
        self.next_id = 1
    
    async def create(self, doctor):
        doctor.id = self.next_id
        self.doctors[self.next_id] = doctor
        self.next_id += 1
        return doctor
    
    async def get_by_id(self, doctor_id):
        return self.doctors.get(doctor_id)
    
    async def get_by_user_id(self, user_id):
        for d in self.doctors.values():
            if d.user_id == user_id:
                return d
        return None
    
    async def get_by_crm(self, crm):
        for d in self.doctors.values():
            if d.crm == crm:
                return d
        return None
    
    async def update(self, doctor):
        self.doctors[doctor.id] = doctor
        return doctor
    
    async def list(self, filters=None, limit=100, offset=0):
        doctors = list(self.doctors.values())
        if filters and "specialty" in filters:
            doctors = [d for d in doctors if filters["specialty"].lower() in d.specialty.lower()]
        if filters and "is_active" in filters:
            doctors = [d for d in doctors if d.is_active == filters["is_active"]]
        return doctors
    
    async def list_by_specialty(self, specialty, limit=100, offset=0):
        return [d for d in self.doctors.values() if specialty.lower() in d.specialty.lower()]


class MockAppointmentRepository:
    """Mock appointment repository for testing."""
    
    def __init__(self):
        self.appointments = {}
        self.next_id = 1
    
    async def create(self, appointment):
        appointment.id = self.next_id
        self.appointments[self.next_id] = appointment
        self.next_id += 1
        return appointment
    
    async def get_by_id(self, appointment_id):
        return self.appointments.get(appointment_id)
    
    async def update(self, appointment):
        self.appointments[appointment.id] = appointment
        return appointment
    
    async def list_by_patient(self, patient_id, status=None, from_date=None, limit=100, offset=0):
        apps = [a for a in self.appointments.values() if a.patient_id == patient_id]
        if status:
            apps = [a for a in apps if a.status == status]
        return apps
    
    async def list_by_doctor(self, doctor_id, status=None, from_date=None, to_date=None, limit=100, offset=0):
        apps = [a for a in self.appointments.values() if a.doctor_id == doctor_id]
        if status:
            apps = [a for a in apps if a.status == status]
        return apps
    
    async def check_conflicts(self, doctor_id, scheduled_at, duration_minutes, exclude_appointment_id=None):
        conflicts = []
        end_time = scheduled_at + timedelta(minutes=duration_minutes)
        
        for app in self.appointments.values():
            if app.doctor_id != doctor_id:
                continue
            if app.id == exclude_appointment_id:
                continue
            if app.status not in ["scheduled", "confirmed"]:
                continue
            
            app_end = app.scheduled_at + timedelta(minutes=app.duration_minutes)
            if (scheduled_at < app_end and app.scheduled_at < end_time):
                conflicts.append(app)
        
        return conflicts


@pytest.mark.asyncio
class TestPatientService:
    """Test Patient service."""
    
    async def test_create_patient_success(self):
        """Test successful patient creation."""
        repo = MockPatientRepository()
        service = PatientService(repo)
        
        from application.services.patient_service import CreatePatientInput
        
        input_data = CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        
        patient = await service.create_patient(input_data)
        assert patient.full_name == "João Silva"
        assert patient.cpf == "529.982.247-25"
    
    async def test_create_patient_duplicate_cpf(self):
        """Test patient creation with duplicate CPF."""
        repo = MockPatientRepository()
        service = PatientService(repo)
        
        from application.services.patient_service import CreatePatientInput
        
        # Create first patient
        input_data = CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        await service.create_patient(input_data)
        
        # Try to create second with same CPF
        input_data2 = CreatePatientInput(
            user_id=uuid4(),
            full_name="Maria Silva",
            cpf="529.982.247-25",
            email="maria@example.com",
            birth_date=date(1990, 5, 15),
            gender="female",
        )
        
        with pytest.raises(PatientAlreadyExistsError):
            await service.create_patient(input_data2)
    
    async def test_get_patient(self):
        """Test getting patient by ID."""
        repo = MockPatientRepository()
        service = PatientService(repo)
        
        from application.services.patient_service import CreatePatientInput
        
        input_data = CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        created = await service.create_patient(input_data)
        
        patient = await service.get_patient(created.id)
        assert patient.full_name == "João Silva"
    
    async def test_add_allergy(self):
        """Test adding allergy to patient."""
        repo = MockPatientRepository()
        service = PatientService(repo)
        
        from application.services.patient_service import CreatePatientInput
        
        input_data = CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        )
        created = await service.create_patient(input_data)
        
        updated = await service.add_allergy(created.id, "Penicilina")
        assert "Penicilina" in updated.allergies


@pytest.mark.asyncio
class TestDoctorService:
    """Test Doctor service."""
    
    async def test_create_doctor_success(self):
        """Test successful doctor creation."""
        repo = MockDoctorRepository()
        service = DoctorService(repo)
        
        from application.services.doctor_service import CreateDoctorInput
        
        input_data = CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria@example.com",
            consultation_fee=Decimal("250.00"),
        )
        
        doctor = await service.create_doctor(input_data)
        assert doctor.full_name == "Dr. Maria Santos"
        assert doctor.crm == "CRM/SP 123456"
    
    async def test_create_doctor_duplicate_crm(self):
        """Test doctor creation with duplicate CRM."""
        repo = MockDoctorRepository()
        service = DoctorService(repo)
        
        from application.services.doctor_service import CreateDoctorInput
        
        # Create first doctor
        input_data = CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Maria Santos",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria@example.com",
        )
        await service.create_doctor(input_data)
        
        # Try to create second with same CRM
        input_data2 = CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. João Silva",
            crm="CRM/SP 123456",
            specialty="Dermatologia",
            email="joao@example.com",
        )
        
        with pytest.raises(DoctorAlreadyExistsError):
            await service.create_doctor(input_data2)
    
    async def test_list_doctors_by_specialty(self):
        """Test listing doctors by specialty."""
        repo = MockDoctorRepository()
        service = DoctorService(repo)
        
        from application.services.doctor_service import CreateDoctorInput
        
        # Create doctors
        await service.create_doctor(CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Cardio 1",
            crm="CRM/SP 111111",
            specialty="Cardiologia",
            email="cardio1@example.com",
        ))
        
        await service.create_doctor(CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Cardio 2",
            crm="CRM/SP 222222",
            specialty="Cardiologia",
            email="cardio2@example.com",
        ))
        
        await service.create_doctor(CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Derma",
            crm="CRM/SP 333333",
            specialty="Dermatologia",
            email="derma@example.com",
        ))
        
        cardiologists = await service.list_doctors_by_specialty("Cardiologia")
        assert len(cardiologists) == 2


@pytest.mark.asyncio
class TestAppointmentService:
    """Test Appointment service."""
    
    async def test_schedule_appointment_success(self):
        """Test successful appointment scheduling."""
        appointment_repo = MockAppointmentRepository()
        patient_repo = MockPatientRepository()
        doctor_repo = MockDoctorRepository()
        
        service = AppointmentService(appointment_repo, patient_repo, doctor_repo)
        
        # Create patient and doctor
        from application.services.patient_service import CreatePatientInput
        from application.services.doctor_service import CreateDoctorInput
        
        patient = await PatientService(patient_repo).create_patient(CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        ))
        
        doctor = await DoctorService(doctor_repo).create_doctor(CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Maria",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria@example.com",
        ))
        
        from application.services.appointment_service import ScheduleAppointmentInput
        
        input_data = ScheduleAppointmentInput(
            patient_id=patient.id,
            doctor_id=doctor.id,
            scheduled_at=datetime.now() + timedelta(days=1),
            duration_minutes=30,
        )
        
        appointment = await service.schedule_appointment(input_data)
        assert appointment.status == "scheduled"
    
    async def test_schedule_appointment_conflict(self):
        """Test appointment scheduling with conflict."""
        appointment_repo = MockAppointmentRepository()
        patient_repo = MockPatientRepository()
        doctor_repo = MockDoctorRepository()
        
        service = AppointmentService(appointment_repo, patient_repo, doctor_repo)
        
        # Create patient and doctor
        from application.services.patient_service import CreatePatientInput
        from application.services.doctor_service import CreateDoctorInput
        
        patient = await PatientService(patient_repo).create_patient(CreatePatientInput(
            user_id=uuid4(),
            full_name="João Silva",
            cpf="529.982.247-25",
            email="joao@example.com",
            birth_date=date(1990, 5, 15),
            gender="male",
        ))
        
        doctor = await DoctorService(doctor_repo).create_doctor(CreateDoctorInput(
            user_id=uuid4(),
            full_name="Dr. Maria",
            crm="CRM/SP 123456",
            specialty="Cardiologia",
            email="maria@example.com",
        ))
        
        from application.services.appointment_service import ScheduleAppointmentInput
        
        # Schedule first appointment
        scheduled_at = datetime.now() + timedelta(days=1)
        await service.schedule_appointment(ScheduleAppointmentInput(
            patient_id=patient.id,
            doctor_id=doctor.id,
            scheduled_at=scheduled_at,
            duration_minutes=30,
        ))
        
        # Try to schedule conflicting appointment
        with pytest.raises(AppointmentConflictError):
            await service.schedule_appointment(ScheduleAppointmentInput(
                patient_id=patient.id + 1,
                doctor_id=doctor.id,
                scheduled_at=scheduled_at,
                duration_minutes=30,
            ))
