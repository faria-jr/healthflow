"""Tests for Appointment entity."""

from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from domain.entities import Appointment
from domain.exceptions import InvalidAppointmentTimeError, AppointmentStatusError


class TestAppointmentEntity:
    """Test Appointment entity."""

    @freeze_time("2026-04-06 12:00:00")
    def test_create_appointment_success(self):
        """Test successful appointment creation."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
        )
        
        assert appointment.patient_id == 1
        assert appointment.doctor_id == 1
        assert appointment.status == "scheduled"
        assert appointment.duration_minutes == 30

    def test_create_appointment_invalid_duration(self):
        """Test appointment creation with invalid duration."""
        future_time = datetime.now() + timedelta(days=1)
        
        with pytest.raises(InvalidAppointmentTimeError):
            Appointment(
                patient_id=1,
                doctor_id=1,
                scheduled_at=future_time,
                duration_minutes=0,
            )

    def test_create_appointment_negative_duration(self):
        """Test appointment creation with negative duration."""
        future_time = datetime.now() + timedelta(days=1)
        
        with pytest.raises(InvalidAppointmentTimeError):
            Appointment(
                patient_id=1,
                doctor_id=1,
                scheduled_at=future_time,
                duration_minutes=-10,
            )

    @freeze_time("2026-04-06 12:00:00")
    def test_create_appointment_in_past(self):
        """Test appointment creation in the past."""
        past_time = datetime.now() - timedelta(days=1)
        
        with pytest.raises(InvalidAppointmentTimeError):
            Appointment(
                patient_id=1,
                doctor_id=1,
                scheduled_at=past_time,
                duration_minutes=30,
            )

    def test_end_time_calculation(self):
        """Test end time calculation."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
        )
        
        expected_end = future_time + timedelta(minutes=30)
        assert appointment.end_time == expected_end

    def test_overlaps_with_same_doctor(self):
        """Test overlap detection with same doctor."""
        base_time = datetime.now() + timedelta(days=1)
        
        appointment1 = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=base_time,
            duration_minutes=30,
        )
        
        # Overlapping appointment
        appointment2 = Appointment(
            patient_id=2,
            doctor_id=1,
            scheduled_at=base_time + timedelta(minutes=15),
            duration_minutes=30,
        )
        
        assert appointment1.overlaps_with(appointment2) is True

    def test_overlaps_with_different_doctor(self):
        """Test overlap detection with different doctor."""
        base_time = datetime.now() + timedelta(days=1)
        
        appointment1 = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=base_time,
            duration_minutes=30,
        )
        
        # Same time, different doctor
        appointment2 = Appointment(
            patient_id=2,
            doctor_id=2,
            scheduled_at=base_time,
            duration_minutes=30,
        )
        
        assert appointment1.overlaps_with(appointment2) is False

    def test_overlaps_non_overlapping(self):
        """Test non-overlapping appointments."""
        base_time = datetime.now() + timedelta(days=1)
        
        appointment1 = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=base_time,
            duration_minutes=30,
        )
        
        # Non-overlapping appointment
        appointment2 = Appointment(
            patient_id=2,
            doctor_id=1,
            scheduled_at=base_time + timedelta(minutes=60),
            duration_minutes=30,
        )
        
        assert appointment1.overlaps_with(appointment2) is False

    @freeze_time("2026-04-06 12:00:00")
    def test_confirm_appointment(self):
        """Test confirming appointment."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            status="scheduled",
        )
        
        appointment.confirm()
        assert appointment.status == "confirmed"

    @freeze_time("2026-04-06 12:00:00")
    def test_complete_appointment(self):
        """Test completing appointment."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            status="confirmed",
        )
        
        appointment.complete()
        assert appointment.status == "completed"

    @freeze_time("2026-04-06 12:00:00")
    def test_cancel_appointment(self):
        """Test cancelling appointment."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            status="scheduled",
        )
        
        appointment.cancel("Paciente solicitou cancelamento")
        assert appointment.status == "cancelled"
        assert appointment.cancellation_reason == "Paciente solicitou cancelamento"

    @freeze_time("2026-04-06 12:00:00")
    def test_invalid_status_transition(self):
        """Test invalid status transition."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            status="scheduled",
        )
        
        # Cannot go from scheduled to completed directly
        with pytest.raises(AppointmentStatusError):
            appointment.transition_to("completed")

    @freeze_time("2026-04-06 12:00:00")
    def test_can_transition_to(self):
        """Test can_transition_to method."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            status="scheduled",
        )
        
        assert appointment.can_transition_to("confirmed") is True
        assert appointment.can_transition_to("cancelled") is True
        assert appointment.can_transition_to("completed") is False

    def test_to_dict(self):
        """Test appointment to dict conversion."""
        future_time = datetime.now() + timedelta(days=1)
        
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            scheduled_at=future_time,
            duration_minutes=30,
            notes="Primeira consulta",
        )
        
        data = appointment.to_dict()
        assert