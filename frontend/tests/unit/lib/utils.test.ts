import { describe, it, expect } from 'vitest'
import { cn, formatDate, formatCurrency, formatCPF, formatPhone } from '@/lib/utils'

describe('cn (className merge)', () => {
  it('merges class names', () => {
    expect(cn('class1', 'class2')).toBe('class1 class2')
  })

  it('handles conditional classes', () => {
    expect(cn('base', true && 'conditional')).toBe('base conditional')
    expect(cn('base', false && 'conditional')).toBe('base')
  })

  it('removes duplicates', () => {
    expect(cn('class1', 'class1')).toBe('class1')
  })
})

describe('formatDate', () => {
  it('formats date string', () => {
    expect(formatDate('2026-04-07')).toBe('07/04/2026')
  })

  it('formats Date object', () => {
    expect(formatDate(new Date('2026-04-07'))).toBe('07/04/2026')
  })
})

describe('formatCurrency', () => {
  it('formats number to BRL currency', () => {
    expect(formatCurrency(250.5)).toBe('R$ 250,50')
  })

  it('formats integer correctly', () => {
    expect(formatCurrency(100)).toBe('R$ 100,00')
  })
})

describe('formatCPF', () => {
  it('formats CPF with dots and dash', () => {
    expect(formatCPF('52998224725')).toBe('529.982.247-25')
  })

  it('handles already formatted CPF', () => {
    expect(formatCPF('529.982.247-25')).toBe('529.982.247-25')
  })
})

describe('formatPhone', () => {
  it('formats mobile phone', () => {
    expect(formatPhone('11987654321')).toBe('(11) 98765-4321')
  })

  it('formats landline phone', () => {
    expect(formatPhone('1132345678')).toBe('(11) 3234-5678')
  })
})
