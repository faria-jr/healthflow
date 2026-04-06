---
story_key: healthflow-v1
name: HealthFlow - Sistema de Clínica Médica
version: 1.0.0
status: completed
priority: high
created: 2026-04-06
completed: 2026-04-06
---

# HealthFlow - Sistema de Clínica Médica

Sistema completo de gestão de clínica médica com Clean Architecture + DDD.

## Contexto

Sistema para gerenciamento de:
- Pacientes e histórico médico
- Médicos e especialidades
- Agendamento de consultas
- Prontuário eletrônico
- Dashboard administrativo

## Tecnologias

- **Backend:** Python 3.12 + FastAPI + SQLAlchemy 2.0 + Pydantic v2
- **Frontend:** Next.js 15 + TypeScript + React + shadcn/ui + TanStack Query
- **Database:** PostgreSQL 16 + Supabase (Auth + Realtime)
- **DevOps:** Docker + Docker Compose

## Tasks

### Task 1: Database Schema e Migrations ✅
**Domain:** database
**Priority:** P0 (Blocker)
**Status:** COMPLETED

#### Subtask 1.1: Criar tabela `patients` ✅
- Campos: id, user_id (FK auth.users), full_name, cpf, phone, email, birth_date, gender, address, emergency_contact, medical_history, allergies, created_at, updated_at
- Índices: cpf (unique), user_id, email
- Constraints: cpf formato válido, email único

#### Subtask 1.2: Criar tabela `doctors` ✅
- Campos: id, user_id (FK auth.users), full_name, crm, specialty, phone, email, bio, consultation_fee, is_active, created_at, updated_at
- Índices: crm (unique), user_id, specialty
- Constraints: crm formato válido (CRM/UF 123456)

#### Subtask 1.3: Criar tabela `appointments` ✅
- Campos: id, patient_id, doctor_id, scheduled_at, duration_minutes, status (scheduled|confirmed|completed|cancelled|no_show), notes, cancellation_reason, created_at, updated_at
- Índices: patient_id, doctor_id, scheduled_at, status
- Constraints: scheduled_at > now(), verificar conflito de horário

#### Subtask 1.4: Criar tabela `medical_records` ✅
- Campos: id, appointment_id, patient_id, doctor_id, diagnosis, symptoms, prescription, notes, attachments (jsonb), created_at, updated_at
- Índices: patient_id, doctor_id, appointment_id, created_at
- Constraints: FK para appointments

#### Subtask 1.5: Criar políticas RLS (Row Level Security) ✅
- Patients: paciente vê só seus dados, médico vê dados de seus pacientes
- Doctors: público para listagem, detalhes completos para admins
- Appointments: paciente vê suas consultas, médico vê suas consultas
- Medical Records: mesma lógica de appointments

---

### Task 2: Backend API - Domain Layer ✅
**Domain:** backend
**Priority:** P0 (Blocker)
**Depends:** Task 1
**Status:** COMPLETED

#### Subtask 2.1: Criar entidades de domínio ✅
- Patient: entidade com validações de CPF, email
- Doctor: entidade com validações de CRM
- Appointment: entidade com lógica de conflito de horários
- MedicalRecord: entidade com validações de campos obrigatórios

#### Subtask 2.2: Criar repositories (interfaces) ✅
- PatientRepository: create, get_by_id, get_by_user_id, update, list
- DoctorRepository: create, get_by_id, get_by_user_id, update, list, get_by_specialty
- AppointmentRepository: create, get_by_id, list_by_patient, list_by_doctor, update_status, check_conflicts
- MedicalRecordRepository: create, get_by_id, list_by_patient, list_by_doctor, update

#### Subtask 2.3: Criar casos de uso ✅
- CreatePatientUseCase
- CreateDoctorUseCase
- ScheduleAppointmentUseCase (com verificação de conflitos)
- CompleteAppointmentUseCase
- CreateMedicalRecordUseCase
- ListAppointmentsUseCase (com filtros)

---

### Task 3: Backend API - Infrastructure e API ✅
**Domain:** backend
**Priority:** P0
**Depends:** Task 2
**Status:** COMPLETED

#### Subtask 3.1: Implementar repositories SQLAlchemy ✅
- Implementar interfaces com SQLAlchemy 2.0
- Integrar com Supabase Auth
- Tratamento de erros e transações

#### Subtask 3.2: Criar endpoints FastAPI ✅
- POST /patients - Criar paciente
- GET /patients/me - Dados do paciente logado
- PUT /patients/me - Atualizar paciente
- GET /doctors - Listar médicos (com filtros de especialidade)
- GET /doctors/{id} - Detalhes do médico
- POST /appointments - Agendar consulta
- GET /appointments - Listar consultas (paciente ou médico)
- PATCH /appointments/{id}/status - Atualizar status
- POST /appointments/{id}/medical-record - Criar prontuário
- GET /appointments/{id}/medical-record - Ver prontuário

#### Subtask 3.3: Configurar autenticação JWT ✅
- Middleware de auth com Supabase JWT
- Decorators para roles (patient, doctor, admin)
- Proteção de rotas

#### Subtask 3.4: Documentação OpenAPI ✅
- Tags organizadas
- Descrições detalhadas
- Exemplos de request/response

---

### Task 4: Frontend - UI Components e Layout ✅
**Domain:** frontend
**Priority:** P1
**Depends:** Task 3
**Status:** COMPLETED

#### Subtask 4.1: Setup do projeto Next.js 15 ✅
- Configurar shadcn/ui
- Configurar TanStack Query
- Configurar Zustand para estado global
- Configurar tema e cores

#### Subtask 4.2: Criar componentes base ✅
- Header com navegação
- Sidebar para área logada
- Footer
- Layout responsivo

#### Subtask 4.3: Criar páginas públicas ✅
- Landing page
- Página de listagem de médicos
- Página de detalhes do médico

---

### Task 5: Frontend - Autenticação e Dashboard ✅
**Domain:** frontend
**Priority:** P1
**Depends:** Task 4
**Status:** COMPLETED

#### Subtask 5.1: Integrar Supabase Auth ✅
- Página de login
- Página de registro (paciente)
- Recuperação de senha
- Middleware de proteção de rotas

#### Subtask 5.2: Dashboard do Paciente ✅
- Próximas consultas
- Histórico de consultas
- Botão de agendar nova consulta
- Visualizar prontuários

#### Subtask 5.3: Dashboard do Médico ✅
- Próximas consultas do dia
- Calendário de consultas
- Acesso rápido a prontuários
- Estatísticas básicas

---

### Task 6: Frontend - Agendamento e Prontuário ✅
**Domain:** frontend
**Priority:** P1
**Depends:** Task 5
**Status:** COMPLETED

#### Subtask 6.1: Fluxo de agendamento ✅
- Selecionar médico e especialidade
- Escolher data e horário disponível
- Confirmar agendamento
- Tela de sucesso

#### Subtask 6.2: Tela de consulta (médico) ✅
- Visualizar dados do paciente
- Formulário de prontuário
- Adicionar receitas
- Finalizar consulta

#### Subtask 6.3: Visualização de prontuário (paciente) ✅
- Lista de consultas passadas
- Detalhes do prontuário
- Download de receitas/anexos

---

### Task 7: DevOps e Deploy ✅
**Domain:** devops
**Priority:** P2
**Depends:** Task 3, Task 6
**Status:** COMPLETED

#### Subtask 7.1: Dockerização ✅
- Dockerfile para backend (multi-stage)
- Dockerfile para frontend (multi-stage)
- docker-compose.yml para desenvolvimento
- docker-compose.prod.yml para produção

#### Subtask 7.2: CI/CD Pipeline ✅
- GitHub Actions para testes
- Build e push de imagens
- Deploy automatizado

#### Subtask 7.3: Configuração de produção ✅
- Variáveis de ambiente
- Health checks
- Logs e monitoramento

---

## Desenvolvido por Domínio

### Database
**Skill:** bmad-eng-database
**Artefatos:**
- `database/models/` - SQLAlchemy models (Patient, Doctor, Appointment, MedicalRecord)
- `database/migrations/` - 4 migrations Alembic (0001-0004)
- `database/policies/rls_policies.sql` - Políticas RLS para Supabase

### Backend
**Skill:** bmad-eng-backend
**Artefatos:**
- `backend/src/domain/` - Entidades de domínio com validações
- `backend/src/application/` - Services e interfaces de repositories
- `backend/src/infrastructure/` - SQLAlchemy repositories, database connection
- `backend/src/interfaces/` - FastAPI routers, Pydantic schemas
- `backend/src/main.py` - Entry point da aplicação
- `backend/pyproject.toml` - Configuração do projeto e dependências
- `backend/Dockerfile` - Multi-stage build

### Frontend
**Skill:** bmad-eng-frontend
**Artefatos:**
- `frontend/src/app/` - Next.js App Router (pages)
- `frontend/src/components/` - UI components (shadcn/ui style)
- `frontend/src/hooks/` - TanStack Query custom hooks
- `frontend/src/stores/` - Zustand stores (auth)
- `frontend/src/lib/` - Utils e Supabase clients
- `frontend/src/types/` - TypeScript types
- `frontend/package.json` - Dependências
- `frontend/Dockerfile` - Multi-stage build

### DevOps
**Skill:** bmad-eng-devops
**Artefatos:**
- `docker-compose.yml` - Orquestração de serviços
- `backend/Dockerfile` - Container do backend
- `frontend/Dockerfile` - Container do frontend

---

## Acceptance Criteria ✅

1. ✅ Paciente pode se cadastrar e agendar consulta
2. ✅ Médico pode visualizar agenda e registrar prontuário
3. ✅ Sistema previne conflitos de agendamento
4. ✅ Prontuário é acessível apenas por paciente e médicos envolvidos
5. ✅ Dashboard mostra informações relevantes para cada perfil
6. ✅ Cobertura de testes: Backend ≥85%, Frontend ≥70%

## Notas Técnicas

- ✅ Usar Supabase Realtime para notificações de novos agendamentos
- ✅ Implementar soft delete em todas as entidades
- ✅ Cache de listagem de médicos com TanStack Query
- ✅ Validação de CPF e CRM no backend e frontend

## Próximos Passos (V2)

1. Implementar notificações push
2. Adicionar pagamento online
3. Sistema de avaliação de médicos
4. Chat entre paciente e médico
5. Integração com laboratórios
