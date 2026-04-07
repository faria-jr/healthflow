"""Integration tests for Patient API."""

import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
class TestPatientAPI:
    """Test Patient API endpoints."""

    async def test_create_patient(self, client):
        """Test POST /patients."""
        response = await client.post("/api/v1/patients", json={
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "full_name": "João Silva",
            "cpf": "529.982.247-25",
            "email": "joao@example.com",
            "birth_date": "1990-05-15",
            "gender": "male",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "João Silva"

    async def test_create_patient_invalid_cpf(self, client):
        """Test POST /patients with invalid CPF."""
        response = await client.post("/api/v1/patients", json={
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "full_name": "João Silva",
            "cpf": "111.111.111-11",
            "email": "joao@example.com",
            "birth_date": "1990-05-15",
            "gender": "male",
        })
        assert response.status_code == 422

    async def test_get_patient(self, client):
        """Test GET /patients/{id}."""
        # First create a patient
        create_response = await client.post("/api/v1/patients", json={
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            "full_name": "Maria Santos",
            "cpf": "987.654.321-00",
            "email": "maria@example.com",
            "birth_date": "1985-03-20",
            "gender": "female",
        })
        patient_id = create_response.json()["data"]["id"]

        # Get the patient
        response = await client.get(f"/api/v1/patients/{patient_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["full_name"] == "Maria Santos"

    async def test_get_patient_not_found(self, client):
        """Test GET /patients/{id} with non-existent ID."""
        response = await client.get("/api/v1/patients/99999")
        assert response.status_code == 404

    async def test_list_patients(self, client):
        """Test GET /patients."""
        response = await client.get("/api/v1/patients")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "patients" in data["data"]
