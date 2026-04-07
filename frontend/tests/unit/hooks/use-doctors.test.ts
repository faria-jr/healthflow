import { describe, it, expect, vi } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useDoctors, useDoctor } from '@/hooks/use-doctors'
import type { Doctor } from '@/types'

// Mock fetch
global.fetch = vi.fn()

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('useDoctors', () => {
  const mockDoctors: Doctor[] = [
    {
      id: 1,
      user_id: 'user-1',
      full_name: 'Dr. Maria',
      crm: 'CRM/SP 123',
      specialty: 'Cardiologia',
      phone: null,
      email: 'maria@example.com',
      bio: null,
      consultation_fee: null,
      is_active: true,
      created_at: '2026-01-01',
      updated_at: '2026-01-01',
    },
  ]

  it('fetches doctors successfully', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ success: true, data: { doctors: mockDoctors } }),
    } as Response)

    const { result } = renderHook(() => useDoctors(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockDoctors)
  })

  it('handles error', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'))

    const { result } = renderHook(() => useDoctors(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
  })
})

describe('useDoctor', () => {
  const mockDoctor: Doctor = {
    id: 1,
    user_id: 'user-1',
    full_name: 'Dr. Maria',
    crm: 'CRM/SP 123',
    specialty: 'Cardiologia',
    phone: null,
    email: 'maria@example.com',
    bio: null,
    consultation_fee: null,
    is_active: true,
    created_at: '2026-01-01',
    updated_at: '2026-01-01',
  }

  it('fetches doctor by id', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ success: true, data: mockDoctor }),
    } as Response)

    const { result } = renderHook(() => useDoctor(1), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(mockDoctor)
  })

  it('does not fetch when id is 0', () => {
    const { result } = renderHook(() => useDoctor(0), {
      wrapper: createWrapper(),
    })

    expect(result.current.isIdle).toBe(true)
  })
})
