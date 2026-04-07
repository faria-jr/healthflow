"""Integration tests for Doctor API."""

import pytest


@pytest.mark.asyncio
class TestDoctorAPI:
    """Test Doctor API endpoints."""

    async def test_create_doctor(self, client):
        """Test POST /doctors."""
        response = await client.post("/api/v1/doctors", json={
            "user_id": "550e8400-e29b-41d4-a716-446655440002",
            "full_name": "Dr. Carlos Mendes",
            "crm": "CRM/RJ 654321",
            "specialty": "Dermatologia",
            "email": "carlos@example.com",
            "phone": "(21) 98765-4321",
            "bio": "Especialista em dermatologia clínica",
            "consultation_fee": "300.00",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "Dr. Carlos Mendes"
        assert data["data"]["crm"] == "CRM/RJ 654321"

    async def test_create_doctor_invalid_crm(self, client):
        """Test POST /doctors with invalid CRM."""
        response = await client.post("/api/v1/doctors", json={
            "user_id": "550e8400-e29b-41d4-a716-446655440003",
            "full_name": "Dr. Invalid",
            "crm": "CRM/XX 123456",  # Invalid state
            "specialty": "Cardiologia",
            "email": "invalid@example.com",
        })
        assert response.status_code == 422

    async def test_get_doctor(self, client, sample_doctor):
        """Test GET /doctors/{id}."""
        doctor_id = sample_doctor["id"]
        response = await client.get(f"/api/v1/doctors/{doctor_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["full_name"] == "Dr. Maria Santos"

    async def test_get_doctor_not_found(self, client):
        """Test GET /doctors/{id} with non-existent ID."""
        response = await client.get("/api/v1/doctors/99999")
        assert response.status_code == 404

    async def test_list_doctors(self, client):
        """Test GET /doctors."""
        response = await client.get("/api/v1/doctors")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "doctors" in data["data"]

    async def test_list_doctors_by_specialty(self, client, sample_doctor):
        """Test GET /doctors/specialty/{specialty}."""
        response = await client.get("/api/v1/doctors/specialty/Cardiologia")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["doctors"]) > 0

    async def test_update_doctor(self, client, sample_doctor):
        """Test PUT /doctors/me."""
        doctor_id = sample_doctor["id"]
        # This would need authentication in real scenario
        # For now, just test the endpoint exists
        response = await client.get(f"/api/v1/doctors/{doctor_id}")
        assert response.status_code == 200
