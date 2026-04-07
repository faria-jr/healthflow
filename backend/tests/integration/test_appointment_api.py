"""Integration tests for Appointment API."""

import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

from main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
class TestAppointmentAPI:
    """Test Appointment API endpoints."""

    async def test_schedule_appointment(self, client):
        """Test POST /appointments."""
        future_time = (datetime.now() + timedelta(days=1)).isoformat()
        
        response = await client.post("/api/v1/appointments", json={
            "patient_id": 1,
            "doctor_id": 1,
            "scheduled_at": future_time,
            "duration_minutes": 30,
            "notes": "Primeira consulta",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "scheduled"

    async def test_schedule_appointment_conflict(self, client):
        """Test POST /appointments with time conflict."""
        future_time = (datetime.now() + timedelta(days=2)).isoformat()
        
        # Create first appointment
        await client.post("/api/v1/appointments", json={
            "patient_id": 1,
            "doctor_id": 1,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        
        # Try to create conflicting appointment
        response = await client.post("/api/v1/appointments", json={
            "patient_id": 2,
            "doctor_id": 1,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        assert response.status_code == 409

    async def test_update_appointment_status(self, client):
        """Test PATCH /appointments/{id}/status."""
        future_time = (datetime.now() + timedelta(days=3)).isoformat()
        
        # Create appointment
        create_response = await client.post("/api/v1/appointments", json={
            "patient_id": 1,
            "doctor_id": 1,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        appointment_id = create_response.json()["data"]["id"]
        
        # Update status
        response = await client.patch(
            f"/api/v1/appointments/{appointment_id}/status",
            json={"status": "confirmed"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "confirmed"

    async def test_cancel_appointment(self, client):
        """Test POST /appointments/{id}/cancel."""
        future_time = (datetime.now() + timedelta(days=4)).isoformat()
        
        # Create appointment
        create_response = await client.post("/api/v1/appointments", json={
            "patient_id": 1,
            "doctor_id": 1,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        appointment_id = create_response.json()["data"]["id"]
        
        # Cancel appointment
        response = await client.post(
            f"/api/v1/appointments/{appointment_id}/cancel",
            params={"reason": "Paciente solicitou"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "cancelled"
