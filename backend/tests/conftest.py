"""Test configuration and fixtures."""

import asyncio
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from domain.entities import Patient, Doctor, Appointment

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/healthflow_test"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def sample_patient_data():
    """Sample patient data for tests."""
    return {
        "user_id": uuid4(),
        "full_name": "João Silva",
        "cpf": "529.982.247-25",
        "email": "joao.silva@example.com",
        "birth_date": date(1990, 5, 15),
        "gender": "male",
        "phone": "(11) 98765-4321",
        "address": "Rua Example, 123",
    }


@pytest.fixture
def sample_doctor_data():
    """Sample doctor data for tests."""
    return {
        "user_id": uuid4(),
        "full_name": "Dr. Maria Santos",
        "crm": "CRM/SP 123456",
        "specialty": "Cardiologia",
        "email": "maria.santos@example.com",
        "phone": "(11) 98765-4321",
        "bio": "Médica cardiologista com 10 anos de experiência",
        "consultation_fee": Decimal("250.00"),
    }


@pytest.fixture
def sample_appointment_data():
    """Sample appointment data for tests."""
    future_date = datetime.now()
    future_date = future_date.replace(day=future_date.day + 1)
    
    return {
        "patient_id": 1,
        "doctor_id": 1,
        "scheduled_at": future_date,
        "duration_minutes": 30,
        "notes": "Primeira consulta",
    }
