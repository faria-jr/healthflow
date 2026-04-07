import { describe, it, expect, vi } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { usePatientAppointments, useDoctorAppointments, useCreateAppointment } from '@/hooks/use-appointments'
import type { Appointment } from '@/types'

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('usePatientAppointments', () => {
  const mockAppointments: Appointment[] = [
    {
      id: 1,
      patient_id: 1,
      doctor_id: 1,
      scheduled_at: '2026-04-10T14:00:00Z',
      end_time: '2026-04-10T14:30:00Z',
      duration_minutes: 30,
      status: 'scheduled',
      notes: null,
      cancellation_reason: null,
      metadata: {},
      created_at: '2026-04-07',
      updated_at: '2026-04-07',
    },
  ]

  it('fetches patient appointments', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ success: true, data: { appointments: mockAppointments } }),
    } as Response)

    const { result } = renderHook(() => usePatientAppointments(1), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockAppointments)
  })

  it('does not fetch when patientId is 0', () => {
    const { result } = renderHook(() => usePatientAppointments(0), {
      wrapper: createWrapper(),
    })

    expect(result.current.isIdle).toBe(true)
  })
})

describe('useDoctorAppointments', () => {
  const mockAppointments: Appointment[] = [
    {
      id: 1,
      patient_id: 1,
      doctor_id: 1,
      scheduled_at: '2026-04-10T14:00:00Z',
      end_time: '2026-04-10T14:30:00Z',
      duration_minutes: 30,
      status: 'confirmed',
      notes: null,
      cancellation_reason: null,
      metadata: {},
      created_at: '2026-04-07',
      updated_at: '2026-04-07',
    },
  ]

  it('fetches doctor appointments', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ success: true, data: { appointments: mockAppointments } }),
    } as Response)

    const { result } = renderHook(() => useDoctorAppointments(1), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockAppointments)
  })
})

describe('useCreateAppointment', () => {
  const mockAppointment: Appointment = {
    id: 1,
    patient_id: 1,
    doctor_id: 1,
    scheduled_at: '2026-04-10T14:00:00Z',
    end_time: '2026-04-10T14:30:00Z',
    duration_minutes: 30,
    status: 'scheduled',
    notes: 'Test',
    cancellation_reason: null,
    metadata: {},
    created_at: '2026-04-07',
    updated_at: '2026-04-07',
  }

  it('creates appointment successfully', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ success: true, data: mockAppointment }),
    } as Response)

    const { result } = renderHook(() => useCreateAppointment(), {
      wrapper: createWrapper(),
    })

    result.current.mutate({
      patient_id: 1,
      doctor_id: 1,
      scheduled_at: '2026-04-10T14:00:00Z',
      duration_minutes: 30,
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockAppointment)
  })

  it('handles creation error', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Conflict'))

    const { result } = renderHook(() => useCreateAppointment(), {
      wrapper: createWrapper(),
    })

    result.current.mutate({
      patient_id: 1,
      doctor_id: 1,
      scheduled_at: '2026-04-10T14:00:00Z',
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
  })
})
