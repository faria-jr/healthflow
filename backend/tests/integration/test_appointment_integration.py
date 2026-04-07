"""Integration tests for Appointment flow."""

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
class TestAppointmentIntegration:
    """Test complete appointment flow."""

    async def test_complete_appointment_flow(self, client, sample_patient, sample_doctor):
        """Test complete appointment lifecycle."""
        patient_id = sample_patient["id"]
        doctor_id = sample_doctor["id"]
        
        # 1. Schedule appointment
        future_time = (datetime.now() + timedelta(days=1)).isoformat()
        response = await client.post("/api/v1/appointments", json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_at": future_time,
            "duration_minutes": 30,
            "notes": "Consulta de rotina",
        })
        assert response.status_code == 201
        appointment = response.json()["data"]
        assert appointment["status"] == "scheduled"
        appointment_id = appointment["id"]
        
        # 2. Confirm appointment
        response = await client.post(f"/api/v1/appointments/{appointment_id}/confirm")
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "confirmed"
        
        # 3. Complete appointment
        response = await client.post(f"/api/v1/appointments/{appointment_id}/complete")
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "completed"

    async def test_appointment_conflict_detection(self, client, sample_patient, sample_doctor):
        """Test that conflicting appointments are rejected."""
        patient_id = sample_patient["id"]
        doctor_id = sample_doctor["id"]
        
        # Schedule first appointment
        future_time = (datetime.now() + timedelta(days=2)).isoformat()
        response1 = await client.post("/api/v1/appointments", json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        assert response1.status_code == 201
        
        # Try to schedule conflicting appointment
        response2 = await client.post("/api/v1/appointments", json={
            "patient_id": patient_id + 1,  # Different patient
            "doctor_id": doctor_id,  # Same doctor
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        assert response2.status_code == 409  # Conflict

    async def test_list_patient_appointments(self, client, sample_patient, sample_doctor):
        """Test listing appointments for a patient."""
        patient_id = sample_patient["id"]
        doctor_id = sample_doctor["id"]
        
        # Create multiple appointments
        for i in range(3):
            future_time = (datetime.now() + timedelta(days=i+3)).isoformat()
            await client.post("/api/v1/appointments", json={
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "scheduled_at": future_time,
                "duration_minutes": 30,
            })
        
        # List appointments
        response = await client.get(f"/api/v1/appointments/patient/{patient_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["appointments"]) >= 3

    async def test_cancel_appointment(self, client, sample_patient, sample_doctor):
        """Test cancelling an appointment."""
        patient_id = sample_patient["id"]
        doctor_id = sample_doctor["id"]
        
        # Create appointment
        future_time = (datetime.now() + timedelta(days=5)).isoformat()
        response = await client.post("/api/v1/appointments", json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_at": future_time,
            "duration_minutes": 30,
        })
        appointment_id = response.json()["data"]["id"]
        
        # Cancel appointment
        response = await client.post(
            f"/api/v1/appointments/{appointment_id}/cancel",
            params={"reason": "Paciente solicitou cancelamento"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "cancelled"
        assert response.json()["data"]["cancellation_reason"] == "Paciente solicitou cancelamento"
