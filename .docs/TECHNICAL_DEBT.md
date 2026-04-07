# Technical Debt - HealthFlow

## Majors Identificados no Code Review BMad

### M1: Race Condition em Agendamento
**Status:** Documentado  
**Prioridade:** Alta  
**Responsável:** Backend Team

**Problema:**
- Verificação de conflitos (`check_conflicts`) e criação (`create`) não são atômicas
- Dois requests simultâneos podem passar na verificação e criar conflito

**Localização:**
- `backend/src/infrastructure/repositories/appointment_repository.py`

**Solução Proposta:**
```python
# Usar SELECT FOR UPDATE
async def create_with_conflict_check(self, appointment):
    async with self._session.begin():
        # Lock rows for this doctor
        await self._session.execute(
            select(AppointmentModel)
            .where(AppointmentModel.doctor_id == appointment.doctor_id)
            .where(AppointmentModel.status.in_(['scheduled', 'confirmed']))
            .for_update()
        )
        
        # Check conflicts
        conflicts = await self.check_conflicts(...)
        if conflicts:
            raise AppointmentConflictError()
        
        # Create appointment
        return await self.create(appointment)
```

**Estimativa:** 4 horas

---

### M2: Validação de CPF Duplicado
**Status:** Documentado  
**Prioridade:** Alta  
**Responsável:** Backend Team

**Problema:**
- Check de existência e INSERT não são atômicos
- Race condition pode criar pacientes com CPF duplicado

**Solução Proposta:**
- Usar constraint UNIQUE no banco + try/except
- Ou usar SELECT FOR UPDATE antes do INSERT

**Estimativa:** 2 horas

---

### M3: N+1 Query em Listagens
**Status:** Parcialmente Corrigido  
**Prioridade:** Média  
**Responsável:** Backend Team

**Problema:**
- `list_by_patient()` e `list_by_doctor()` sem eager loading
- Causa N+1 queries para relacionamentos

**Solução Aplicada:**
- Adicionado `selectinload()` nos métodos

**Verificação:**
```python
# Verificar se selectinload está presente
grep -n "selectinload" backend/src/infrastructure/repositories/appointment_repository.py
```

**Status:** ✅ Corrigido

---

### M4: Missing Pagination
**Status:** Documentado  
**Prioridade:** Média  
**Responsável:** Backend Team

**Problema:**
- `limit=100` hardcoded
- Sem cursor-based pagination para grandes datasets

**Solução Proposta:**
```python
# Implementar cursor-based pagination
async def list_by_patient(
    self,
    patient_id: int,
    cursor: Optional[str] = None,
    limit: int = 20,
):
    query = select(AppointmentModel).where(...)
    
    if cursor:
        decoded = decode_cursor(cursor)
        query = query.where(AppointmentModel.id > decoded)
    
    query = query.limit(limit + 1)  # +1 to check if has_more
    results = await self._session.execute(query)
    
    appointments = results.scalars().all()
    has_more = len(appointments) > limit
    
    return {
        "items": appointments[:limit],
        "next_cursor": encode_cursor(appointments[-1].id) if has_more else None,
    }
```

**Estimativa:** 6 horas

---

### M5: Frontend Sem Error Boundaries
**Status:** Documentado  
**Prioridade:** Média  
**Responsável:** Frontend Team

**Problema:**
- Sem `error.tsx` ou tratamento global de erros
- Erros não capturados podem quebrar a aplicação

**Solução Proposta:**
```tsx
// frontend/src/app/error.tsx
'use client'

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="error-container">
      <h2>Algo deu errado!</h2>
      <button onClick={reset}>Tentar novamente</button>
    </div>
  )
}
```

**Estimativa:** 2 horas

---

### M6: Hardcoded User ID
**Status:** Documentado  
**Prioridade:** Baixa  
**Responsável:** Frontend Team

**Problema:**
- `const patientId = 1; // TODO: Get from user context`

**Solução Proposta:**
- Integrar com auth store
- Usar context ou hook para obter user atual

**Estimativa:** 1 hora

---

### M7: Frontend Sem React.memo
**Status:** Documentado  
**Prioridade:** Baixa  
**Responsável:** Frontend Team

**Problema:**
- Componentes podem re-renderizar desnecessariamente

**Solução Proposta:**
```tsx
const DoctorCard = React.memo(function DoctorCard({ doctor }) {
  // component logic
})
```

**Estimativa:** 1 hora

---

## 📊 Resumo

| Major | Status | Estimativa | Prioridade |
|-------|--------|------------|------------|
| M1: Race Condition | Documentado | 4h | Alta |
| M2: CPF Duplicado | Documentado | 2h | Alta |
| M3: N+1 Queries | ✅ Corrigido | - | Média |
| M4: Pagination | Documentado | 6h | Média |
| M5: Error Boundaries | Documentado | 2h | Média |
| M6: Hardcoded ID | Documentado | 1h | Baixa |
| M7: React.memo | Documentado | 1h | Baixa |

**Total Estimado:** 16 horas

---

## Próximos Passos

1. **Sprint 1:** M1, M2 (Race conditions) - 6h
2. **Sprint 2:** M4 (Pagination) - 6h
3. **Sprint 3:** M5, M6, M7 (Frontend) - 4h
