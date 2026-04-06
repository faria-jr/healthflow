"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { Appointment, ApiResponse, AppointmentStatus } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Query keys
export const appointmentKeys = {
  all: ["appointments"] as const,
  lists: () => [...appointmentKeys.all, "list"] as const,
  patient: (patientId: number) =>
    [...appointmentKeys.lists(), "patient", patientId] as const,
  doctor: (doctorId: number) =>
    [...appointmentKeys.lists(), "doctor", doctorId] as const,
  detail: (id: number) => [...appointmentKeys.all, "detail", id] as const,
};

// API functions
async function fetchPatientAppointments(
  patientId: number
): Promise<Appointment[]> {
  const response = await fetch(
    `${API_URL}/api/v1/appointments/patient/${patientId}`
  );
  const data: ApiResponse<{ appointments: Appointment[] }> =
    await response.json();
  return data.data?.appointments || [];
}

async function fetchDoctorAppointments(
  doctorId: number
): Promise<Appointment[]> {
  const response = await fetch(
    `${API_URL}/api/v1/appointments/doctor/${doctorId}`
  );
  const data: ApiResponse<{ appointments: Appointment[] }> =
    await response.json();
  return data.data?.appointments || [];
}

interface CreateAppointmentInput {
  patient_id: number;
  doctor_id: number;
  scheduled_at: string;
  duration_minutes?: number;
  notes?: string;
}

async function createAppointment(
  input: CreateAppointmentInput
): Promise<Appointment> {
  const response = await fetch(`${API_URL}/api/v1/appointments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  const data: ApiResponse<Appointment> = await response.json();
  if (!data.success || !data.data) {
    throw new Error(data.error || "Failed to create appointment");
  }
  return data.data;
}

async function updateAppointmentStatus(
  appointmentId: number,
  status: AppointmentStatus,
  reason?: string
): Promise<Appointment> {
  const response = await fetch(
    `${API_URL}/api/v1/appointments/${appointmentId}/status`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, reason }),
    }
  );
  const data: ApiResponse<Appointment> = await response.json();
  if (!data.success || !data.data) {
    throw new Error(data.error || "Failed to update appointment");
  }
  return data.data;
}

// Hooks
export function usePatientAppointments(patientId: number) {
  return useQuery({
    queryKey: appointmentKeys.patient(patientId),
    queryFn: () => fetchPatientAppointments(patientId),
    enabled: !!patientId,
  });
}

export function useDoctorAppointments(doctorId: number) {
  return useQuery({
    queryKey: appointmentKeys.doctor(doctorId),
    queryFn: () => fetchDoctorAppointments(doctorId),
    enabled: !!doctorId,
  });
}

export function useCreateAppointment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAppointment,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.patient(data.patient_id),
      });
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.doctor(data.doctor_id),
      });
    },
  });
}

export function useUpdateAppointmentStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      appointmentId,
      status,
      reason,
    }: {
      appointmentId: number;
      status: AppointmentStatus;
      reason?: string;
    }) => updateAppointmentStatus(appointmentId, status, reason),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.patient(data.patient_id),
      });
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.doctor(data.doctor_id),
      });
    },
  });
}
