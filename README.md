# 🏥 HealthFlow - Sistema de Clínica Médica

Sistema completo de gestão de clínica médica com Clean Architecture + DDD.

## ✨ Funcionalidades

- **👤 Pacientes**: Cadastro completo com histórico médico e alergias
- **👨‍⚕️ Médicos**: Cadastro com especialidades, CRM e valores de consulta
- **📅 Agendamento**: Sistema inteligente com verificação de conflitos
- **📋 Prontuário Eletrônico**: Registro de consultas, diagnósticos e receitas
- **🔐 Autenticação**: Integração com Supabase Auth (JWT)
- **📊 Dashboard**: Visão geral para pacientes e médicos

## 🏗️ Arquitetura

```
healthflow/
├── backend/              # FastAPI + SQLAlchemy
│   ├── src/
│   │   ├── domain/       # Entidades e regras de negócio
│   │   ├── application/  # Casos de uso
│   │   ├── infrastructure/ # Repositories, DB, Auth
│   │   └── interfaces/   # FastAPI routers
│   └── tests/
├── frontend/             # Next.js 15 + React 19
│   ├── src/
│   │   ├── app/          # App Router
│   │   ├── components/   # UI Components
│   │   ├── hooks/        # TanStack Query hooks
│   │   └── stores/       # Zustand stores
│   └── tests/
├── database/             # SQLAlchemy models + Alembic
│   ├── models/
│   ├── migrations/
│   └── policies/         # RLS policies
└── docker-compose.yml
```

## 🚀 Tecnologias

### Backend
- **Python 3.12** + FastAPI
- **SQLAlchemy 2.0** + Alembic
- **Pydantic V2** para validação
- **PostgreSQL 16** + Supabase
- **TDD** com pytest (cobertura ≥85%)

### Frontend
- **Next.js 15** + React 19
- **TypeScript 5.x**
- **Tailwind CSS** + shadcn/ui
- **TanStack Query** para data fetching
- **Zustand** para estado global
- **Supabase Auth** para autenticação

## 📦 Instalação

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+ (para desenvolvimento local)
- Python 3.12+ (para desenvolvimento local)

### Com Docker (Recomendado)

```bash
# Clone o repositório
git clone <repo-url>
cd healthflow

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais do Supabase

# Inicie os serviços
docker-compose up -d

# Acesse:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Desenvolvimento Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Rode as migrations
alembic upgrade head

# Inicie o servidor
uvicorn src.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install

# Configure .env.local
cp .env.example .env.local

# Inicie o servidor
npm run dev
```

## 🧪 Testes

### Backend
```bash
cd backend
pytest --cov=src --cov-report=html
```

### Frontend
```bash
cd frontend
npm run test:coverage
```

## 📚 API Endpoints

### Pacientes
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/patients` | Criar paciente |
| GET | `/api/v1/patients/me` | Dados do paciente logado |
| GET | `/api/v1/patients/{id}` | Buscar paciente |
| PUT | `/api/v1/patients/me` | Atualizar paciente |

### Médicos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/doctors` | Criar médico |
| GET | `/api/v1/doctors` | Listar médicos |
| GET | `/api/v1/doctors/{id}` | Buscar médico |
| GET | `/api/v1/doctors/specialty/{specialty}` | Filtrar por especialidade |

### Consultas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/appointments` | Agendar consulta |
| GET | `/api/v1/appointments/{id}` | Buscar consulta |
| PATCH | `/api/v1/appointments/{id}/status` | Atualizar status |
| POST | `/api/v1/appointments/{id}/cancel` | Cancelar |

## 🔐 Variáveis de Ambiente

```env
# Backend
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/healthflow
SECRET_KEY=your-secret-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

Desenvolvido com ❤️ usando Clean Architecture + DDD
