# HealthFlow Backend

Backend API para o Sistema de Clínica Médica HealthFlow.

## Tecnologias

- **Python 3.12+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy 2.0** - ORM para PostgreSQL
- **Pydantic V2** - Validação de dados
- **Alembic** - Migrations de banco de dados
- **Supabase** - PostgreSQL + Auth

## Arquitetura

```
src/
├── config/              # Configurações (Pydantic Settings)
├── domain/              # Entidades, Value Objects, Exceções
│   ├── entities/        # Patient, Doctor, Appointment, MedicalRecord
│   └── exceptions.py    # Exceções de domínio
├── application/         # Casos de uso / Serviços
│   ├── services/        # PatientService, DoctorService, etc.
│   ├── dtos/            # Data Transfer Objects
│   └── interfaces/      # Interfaces de repositórios
├── infrastructure/      # Implementações técnicas
│   ├── repositories/    # SQLAlchemy repositories
│   ├── database/        # Conexão com banco
│   └── auth/            # Autenticação
├── interfaces/          # FastAPI
│   ├── routers/         # Endpoints
│   ├── schemas/         # Pydantic schemas
│   └── middleware/      # Middlewares
└── main.py              # Entry point
```

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

## Variáveis de Ambiente

```env
# App
APP_NAME=HealthFlow API
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/healthflow
DATABASE_ECHO=false

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## Executando

```bash
# Desenvolvimento
uvicorn src.main:app --reload

# Produção
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Verificar tipos
mypy src --strict

# Linting
ruff check src
ruff format src
```

## API Endpoints

### Pacientes
- `POST /api/v1/patients` - Criar paciente
- `GET /api/v1/patients/me` - Dados do paciente logado
- `GET /api/v1/patients/{id}` - Buscar paciente por ID
- `PUT /api/v1/patients/me` - Atualizar paciente
- `POST /api/v1/patients/me/allergies` - Adicionar alergia
- `DELETE /api/v1/patients/me/allergies` - Remover alergia

### Médicos
- `POST /api/v1/doctors` - Criar médico
- `GET /api/v1/doctors/me` - Dados do médico logado
- `GET /api/v1/doctors/{id}` - Buscar médico por ID
- `GET /api/v1/doctors` - Listar médicos
- `GET /api/v1/doctors/specialty/{specialty}` - Listar por especialidade
- `PUT /api/v1/doctors/me` - Atualizar médico

### Consultas
- `POST /api/v1/appointments` - Agendar consulta
- `GET /api/v1/appointments/{id}` - Buscar consulta
- `PATCH /api/v1/appointments/{id}/status` - Atualizar status
- `POST /api/v1/appointments/{id}/confirm` - Confirmar
- `POST /api/v1/appointments/{id}/complete` - Completar
- `POST /api/v1/appointments/{id}/cancel` - Cancelar
- `GET /api/v1/appointments/patient/{patient_id}` - Listar do paciente
- `GET /api/v1/appointments/doctor/{doctor_id}` - Listar do médico

## Documentação

Acesse `/docs` para documentação interativa (Swagger UI) ou `/redoc` para ReDoc.
