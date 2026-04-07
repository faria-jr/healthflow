---
story_key: healthflow-v2
name: HealthFlow Enhanced - Epic V2
version: 2.0.0
status: in_progress
priority: high
created: 2026-04-07
---

# HealthFlow Enhanced - Epic V2

Funcionalidades avançadas para o sistema de clínica médica.

## Contexto

Extensão do HealthFlow v1 com recursos de notificação, pagamento, avaliação, chat e integração com laboratórios.

## Tecnologias Adicionais

- **Notifications:** Firebase Cloud Messaging, Twilio (SMS), SendGrid (Email)
- **Payments:** Stripe / Pagar.me
- **Real-time:** WebSocket (Socket.io) + Redis
- **File Storage:** Supabase Storage / AWS S3
- **Queue:** Redis / Celery (background jobs)

## Tasks

### Task 1: Sistema de Notificações Push
**Domain:** backend + devops
**Priority:** P1

#### Subtask 1.1: Configurar Firebase Cloud Messaging
- Setup projeto Firebase
- Configurar service account
- Adicionar credenciais ao .env

#### Subtask 1.2: Criar tabela `notification_preferences`
- Campos: id, user_id, email_enabled, sms_enabled, push_enabled, reminder_hours
- Índices: user_id

#### Subtask 1.3: Criar tabela `notifications`
- Campos: id, user_id, type (email|sms|push), title, body, data, status, sent_at, read_at
- Índices: user_id, status, created_at

#### Subtask 1.4: Implementar serviço de notificações
- Enviar email via SendGrid
- Enviar SMS via Twilio
- Enviar push via FCM
- Queue com Celery + Redis

#### Subtask 1.5: Criar triggers de notificação
- Lembrete de consulta (24h antes)
- Confirmação de agendamento
- Cancelamento de consulta
- Novo prontuário disponível

#### Subtask 1.6: Frontend - Tela de preferências
- Toggle para email/SMS/push
- Configurar horas de lembrete
- Testar notificações

---

### Task 2: Pagamento Online
**Domain:** backend + frontend
**Priority:** P1

#### Subtask 2.1: Integrar Stripe/Pagar.me
- Configurar SDK
- Criar webhook handlers
- Adicionar credenciais ao .env

#### Subtask 2.2: Criar tabela `payments`
- Campos: id, appointment_id, patient_id, amount, currency, status, provider, provider_payment_id, paid_at, refunded_at
- Índices: appointment_id, patient_id, status

#### Subtask 2.3: Criar endpoints de pagamento
- POST /payments/intent - Criar intenção de pagamento
- POST /payments/confirm - Confirmar pagamento
- POST /payments/refund - Reembolsar
- GET /payments/{id} - Status do pagamento

#### Subtask 2.4: Implementar webhook handlers
- payment_intent.succeeded
- payment_intent.payment_failed
- charge.refunded

#### Subtask 2.5: Frontend - Fluxo de pagamento
- Tela de checkout
- Integração com Stripe Elements
- Confirmação de pagamento
- Histórico de pagamentos

---

### Task 3: Sistema de Avaliação
**Domain:** backend + frontend
**Priority:** P2

#### Subtask 3.1: Criar tabela `reviews`
- Campos: id, doctor_id, patient_id, appointment_id, rating (1-5), comment, is_anonymous, status, created_at
- Índices: doctor_id, patient_id, appointment_id, status
- Constraints: UNIQUE(appointment_id) - um review por consulta

#### Subtask 3.2: Implementar serviço de reviews
- Create review (após consulta completada)
- Update review
- Delete review (soft delete)
- Moderar reviews (aprovar/rejeitar)

#### Subtask 3.3: Criar endpoints de reviews
- POST /reviews - Criar avaliação
- GET /reviews/doctor/{doctor_id} - Listar avaliações do médico
- GET /reviews/me - Minhas avaliações
- PATCH /reviews/{id}/moderate - Moderar (admin)

#### Subtask 3.4: Calcular métricas de reviews
- Média de rating por médico
- Total de reviews
- Distribuição de ratings (1-5 estrelas)

#### Subtask 3.5: Frontend - Componentes de review
- Star rating component
- Formulário de avaliação
- Lista de reviews
- Resumo de métricas

---

### Task 4: Chat em Tempo Real
**Domain:** backend + frontend + devops
**Priority:** P2

#### Subtask 4.1: Configurar WebSocket (Socket.io)
- Setup servidor Socket.io
- Integrar com FastAPI
- Configurar Redis adapter

#### Subtask 4.2: Criar tabela `chat_messages`
- Campos: id, appointment_id, sender_id, sender_type (patient|doctor), content, attachments, sent_at, read_at
- Índices: appointment_id, sender_id, sent_at

#### Subtask 4.3: Implementar handlers de chat
- Join room (appointment)
- Send message
- Mark as read
- Typing indicator

#### Subtask 4.4: Implementar autorização de chat
- Apenas participantes da consulta podem acessar
- Verificar se consulta está agendada/confirmada

#### Subtask 4.5: Frontend - Interface de chat
- Chat window component
- Lista de mensagens
- Input com emoji
- Indicador de digitação
- Notificações de nova mensagem

---

### Task 5: Integração com Laboratórios
**Domain:** backend + frontend + devops
**Priority:** P2

#### Subtask 5.1: Configurar Supabase Storage
- Setup buckets para exames
- Configurar políticas de acesso
- Limite de tamanho (10MB por arquivo)

#### Subtask 5.2: Criar tabela `lab_results`
- Campos: id, patient_id, doctor_id, appointment_id, lab_name, test_type, result_summary, file_url, file_name, file_size, status, uploaded_at
- Índices: patient_id, doctor_id, appointment_id, status

#### Subtask 5.3: Implementar upload de exames
- Endpoint para upload (presigned URL)
- Validação de tipo (PDF, JPG, PNG)
- Scan de vírus (ClamAV)

#### Subtask 5.4: Implementar visualização de exames
- Listar exames do paciente
- Download seguro (temp URL)
- Preview no browser

#### Subtask 5.5: Frontend - Gestão de exames
- Upload component com drag-drop
- Lista de exames
- Visualizador de PDF/imagem
- Compartilhar com médico

---

## Acceptance Criteria

1. Paciente recebe notificações push/email/SMS antes das consultas
2. Paciente pode pagar consulta online via cartão
3. Paciente pode avaliar médico após consulta
4. Paciente e médico podem conversar via chat em tempo real
5. Paciente pode fazer upload de exames laboratoriais
6. Médico pode visualizar e baixar exames dos pacientes
7. Cobertura de testes: Backend ≥85%, Frontend ≥70%

## Notas Técnicas

- Usar Celery + Redis para fila de notificações
- WebSocket com autenticação JWT
- Pagamentos com idempotência (evitar duplicatas)
- Reviews só podem ser feitas após consulta completada
- Exames criptografados em repouso (AES-256)
