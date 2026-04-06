"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { Doctor, ApiResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Query keys
export const doctorKeys = {
  all: ["doctors"] as const,
  lists: () => [...doctorKeys.all, "list"] as const,
  list: (filters: string) => [...doctorKeys.lists(), { filters }] as const,
  details: () => [...doctorKeys.all, "detail"] as const,
  detail: (id: number) => [...doctorKeys.details(), id] as const,
};

// API functions
async function fetchDoctors(): Promise<Doctor[]> {
  const response = await fetch(`${API_URL}/api/v1/doctors`);
  const data: ApiResponse<{ doctors: Doctor[] }> = await response.json();
  return data.data?.doctors || [];
}

async function fetchDoctorById(id: number): Promise<Doctor | null> {
  const response = await fetch(`${API_URL}/api/v1/doctors/${id}`);
  const data: ApiResponse<Doctor> = await response.json();
  return data.data;
}

async function fetchDoctorsBySpecialty(specialty: string): Promise<Doctor[]> {
  const response = await fetch(
    `${API_URL}/api/v1/doctors/specialty/${encodeURIComponent(specialty)}`
  );
  const data: ApiResponse<{ doctors: Doctor[] }> = await response.json();
  return data.data?.doctors || [];
}

// Hooks
export function useDoctors() {
  return useQuery({
    queryKey: doctorKeys.lists(),
    queryFn: fetchDoctors,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useDoctor(id: number) {
  return useQuery({
    queryKey: doctorKeys.detail(id),
    queryFn: () => fetchDoctorById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
}

export function useDoctorsBySpecialty(specialty: string) {
  return useQuery({
    queryKey: [...doctorKeys.lists(), "specialty", specialty],
    queryFn: () => fetchDoctorsBySpecialty(specialty),
    enabled: !!specialty,
    staleTime: 5 * 60 * 1000,
  });
}
