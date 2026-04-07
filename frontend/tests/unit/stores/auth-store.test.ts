import { describe, it, expect, vi } from 'vitest'
import { useAuthStore } from '@/stores/auth-store'
import type { User } from '@/types'

describe('useAuthStore', () => {
  const mockUser: User = {
    id: 'user-123',
    email: 'test@example.com',
    role: 'patient',
  }

  it('initial state is correct', () => {
    const state = useAuthStore.getState()
    expect(state.user).toBeNull()
    expect(state.isLoading).toBe(true)
  })

  it('setUser updates user state', () => {
    useAuthStore.getState().setUser(mockUser)
    expect(useAuthStore.getState().user).toEqual(mockUser)
    expect(useAuthStore.getState().isLoading).toBe(false)
  })

  it('setLoading updates loading state', () => {
    useAuthStore.getState().setLoading(false)
    expect(useAuthStore.getState().isLoading).toBe(false)
    
    useAuthStore.getState().setLoading(true)
    expect(useAuthStore.getState().isLoading).toBe(true)
  })

  it('logout clears user state', () => {
    // First set a user
    useAuthStore.getState().setUser(mockUser)
    expect(useAuthStore.getState().user).not.toBeNull()
    
    // Then logout
    useAuthStore.getState().logout()
    expect(useAuthStore.getState().user).toBeNull()
    expect(useAuthStore.getState().isLoading).toBe(false)
  })

  it('persists state to localStorage', () => {
    // Set user
    useAuthStore.getState().setUser(mockUser)
    
    // Check localStorage
    const stored = localStorage.getItem('auth-storage')
    expect(stored).toContain('test@example.com')
  })
})
