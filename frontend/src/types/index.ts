export interface Patient {
  id: number;
  user_id: string;
  full_name: string;
  cpf: string;
  phone: string | null;
  email: string;
  birth_date: string;
  gender: "male" | "female" | "other" | "prefer_not_to_say";
  address: string | null;
  emergency_contact: Record<string, unknown> | null;
  medical_history: Record<string, unknown>;
  allergies: string[];
  created_at: string;
  updated_at: string;
}

export interface Doctor {
  id: number;
  user_id: string;
  full_name: string;
  crm: string;
  specialty: string;
  phone: string | null;
  email: string;
  bio: string | null;
  consultation_fee: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type AppointmentStatus =
  | "scheduled"
  | "confirmed"
  | "completed"
  | "cancelled"
  | "no_show";

export interface Appointment {
  id: number;
  patient_id: number;
  doctor_id: number;
  scheduled_at: string;
  end_time: string;
  duration_minutes: number;
  status: AppointmentStatus;
  notes: string | null;
  cancellation_reason: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  // Joined fields
  patient?: Patient;
  doctor?: Doctor;
}

export interface MedicalRecord {
  id: number;
  appointment_id: number;
  patient_id: number;
  doctor_id: number;
  diagnosis: string | null;
  symptoms: string | null;
  prescription: string | null;
  notes: string | null;
  attachments: Attachment[];
  created_at: string;
  updated_at: string;
}

export interface Attachment {
  name: string;
  url: string;
  type: string;
  size?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  meta?: {
    total: number;
    limit: number;
    offset: number;
  };
}

export interface User {
  id: string;
  email: string;
  role: "patient" | "doctor" | "admin";
}
