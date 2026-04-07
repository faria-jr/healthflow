import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { AppointmentCard } from '@/components/appointment-card'
import type { Appointment } from '@/types'

describe('AppointmentCard', () => {
  const mockAppointment: Appointment = {
    id: 1,
    patient_id: 1,
    doctor_id: 1,
    scheduled_at: '2026-04-10T14:00:00Z',
    end_time: '2026-04-10T14:30:00Z',
    duration_minutes: 30,
    status: 'scheduled',
    notes: 'Primeira consulta',
    cancellation_reason: null,
    metadata: {},
    created_at: '2026-04-07T00:00:00Z',
    updated_at: '2026-04-07T00:00:00Z',
    doctor: {
      id: 1,
      user_id: 'user-1',
      full_name: 'Dr. Maria Santos',
      crm: 'CRM/SP 123456',
      specialty: 'Cardiologia',
      phone: null,
      email: 'maria@example.com',
      bio: null,
      consultation_fee: 250.00,
      is_active: true,
      created_at: '2026-01-01',
      updated_at: '2026-01-01',
    },
  }

  it('renders appointment date and time', () => {
    render(<AppointmentCard appointment={mockAppointment} showDoctor />)
    expect(screen.getByText(/10\/04\/2026/)).toBeInTheDocument()
  })

  it('renders doctor name when showDoctor is true', () => {
    render(<AppointmentCard appointment={mockAppointment} showDoctor />)
    expect(screen.getByText(/Dr\. Maria Santos/)).toBeInTheDocument()
    expect(screen.getByText(/Cardiologia/)).toBeInTheDocument()
  })

  it('does not render doctor when showDoctor is false', () => {
    render(<AppointmentCard appointment={mockAppointment} showDoctor={false} />)
    expect(screen.queryByText(/Dr\. Maria Santos/)).not.toBeInTheDocument()
  })

  it('renders appointment status', () => {
    render(<AppointmentCard appointment={mockAppointment} />)
    expect(screen.getByText('Agendada')).toBeInTheDocument()
  })

  it('renders duration', () => {
    render(<AppointmentCard appointment={mockAppointment} />)
    expect(screen.getByText('30 minutos')).toBeInTheDocument()
  })

  it('renders notes when provided', () => {
    render(<AppointmentCard appointment={mockAppointment} />)
    expect(screen.getByText('Primeira consulta')).toBeInTheDocument()
  })

  it('calls onCancel when cancel button is clicked', () => {
    const handleCancel = vi.fn()
    render(
      <AppointmentCard 
        appointment={mockAppointment} 
        onCancel={handleCancel}
      />
    )
    
    const cancelButton = screen.getByText('Cancelar')
    fireEvent.click(cancelButton)
    expect(handleCancel).toHaveBeenCalledTimes(1)
  })

  it('calls onConfirm when confirm button is clicked', () => {
    const handleConfirm = vi.fn()
    render(
      <AppointmentCard 
        appointment={mockAppointment} 
        onConfirm={handleConfirm}
      />
    )
    
    const confirmButton = screen.getByText('Confirmar')
    fireEvent.click(confirmButton)
    expect(handleConfirm).toHaveBeenCalledTimes(1)
  })

  it('renders completed status correctly', () => {
    const completedAppointment = { ...mockAppointment, status: 'completed' as const }
    render(<AppointmentCard appointment={completedAppointment} />)
    expect(screen.getByText('Concluída')).toBeInTheDocument()
  })

  it('renders cancelled status correctly', () => {
    const cancelledAppointment = { 
      ...mockAppointment, 
      status: 'cancelled' as const,
      cancellation_reason: 'Paciente solicitou'
    }
    render(<AppointmentCard appointment={cancelledAppointment} />)
    expect(screen.getByText('Cancelada')).toBeInTheDocument()
  })
})
