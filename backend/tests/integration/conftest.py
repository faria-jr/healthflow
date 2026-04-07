"""Integration test configuration."""

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from main import app

# Test database
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/healthflow_test"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncSession:
    """Create test database session."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client():
    """Create test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def sample_patient(client):
    """Create a sample patient for tests."""
    response = await client.post("/api/v1/patients", json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "full_name": "João Silva",
        "cpf": "529.982.247-25",
        "email": "joao@example.com",
        "birth_date": "1990-05-15",
        "gender": "male",
    })
    return response.json()["data"]


@pytest_asyncio.fixture
async def sample_doctor(client):
    """Create a sample doctor for tests."""
    response = await client.post("/api/v1/doctors", json={
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "full_name": "Dr. Maria Santos",
        "crm": "CRM/SP 123456",
        "specialty": "Cardiologia",
        "email": "maria@example.com",
    })
    return response.json()["data"]
