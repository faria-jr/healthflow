import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { DoctorCard } from '@/components/doctor-card'
import type { Doctor } from '@/types'

describe('DoctorCard', () => {
  const mockDoctor: Doctor = {
    id: 1,
    user_id: 'user-123',
    full_name: 'Dr. Maria Santos',
    crm: 'CRM/SP 123456',
    specialty: 'Cardiologia',
    phone: '(11) 98765-4321',
    email: 'maria@example.com',
    bio: 'Especialista em cardiologia',
    consultation_fee: 250.00,
    is_active: true,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
  }

  it('renders doctor name', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('Dr. Maria Santos')).toBeInTheDocument()
  })

  it('renders doctor specialty', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('Cardiologia')).toBeInTheDocument()
  })

  it('renders doctor CRM', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('CRM/SP 123456')).toBeInTheDocument()
  })

  it('renders consultation fee', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('R$ 250,00')).toBeInTheDocument()
  })

  it('renders agendar button', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('Agendar')).toBeInTheDocument()
  })

  it('renders bio when provided', () => {
    render(<DoctorCard doctor={mockDoctor} />)
    expect(screen.getByText('Especialista em cardiologia')).toBeInTheDocument()
  })
})
