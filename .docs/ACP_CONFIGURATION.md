# Configuração ACP (Agent Control Protocol) - HealthFlow

## Status da Configuração

### ✅ Configurações Aplicadas

#### 1. Plugin ACPX Runtime Habilitado
```bash
openclaw plugins enable acpx
```
**Status:** `loaded` ✅

#### 2. Agentes BMad Configurados
Arquivo: `~/.openclaw/openclaw.json`

```json
{
  "agents": {
    "list": [
      {
        "id": "bmad-master",
        "name": "BMad Master",
        "workspace": "~/.openclaw/workspace-bmad-master",
        "tools": {
          "allow": [
            "read", "write", "edit", "exec",
            "sessions_spawn", "sessions_send",
            "bmad-method"
          ]
        }
      },
      {
        "id": "bmad-dev",
        "name": "BMad Development Team",
        "workspace": "~/.openclaw/workspace-bmad-dev",
        "tools": {
          "allow": [
            "read", "write", "edit", "exec",
            "sessions_spawn", "sessions_send",
            "web_search", "web_fetch"
          ]
        }
      }
    ],
    "defaults": {
      "subagents": {
        "maxConcurrent": 8
      }
    }
  }
}
```

#### 3. Skills BMad Habilitadas
Todas as skills estão `enabled: true`:
- `bmad-eng-backend`
- `bmad-eng-frontend`
- `bmad-eng-database`
- `bmad-eng-devops`
- `bmad-qa-bug-founder`
- `bmad-qa-code-quality`
- `bmad-qa-performance`
- `bmad-qa-security`
- `bmad-qa-tdd`
- `bmad-qa-consolidator`
- `bmad-dev-dispatcher`
- `bmad-code-review`

#### 4. ACP Default Agent Configurado
```bash
openclaw config set acp.defaultAgent "bmad-qa-bug-founder"
```

#### 5. Plugin BMad Method Carregado
```
BMad Method plugin loaded
Registered 7 tools:
- bmad_init_project
- bmad_list_workflows
- bmad_start_workflow
- bmad_load_step
- bmad_save_artifact
- bmad_complete_workflow
- bmad_get_state
```

---

## ❌ Problemas Identificados

### Erro: "ACP runtime backend is not configured"

**Causa:** O plugin `acpx` está carregado, mas o runtime ACP não está funcionando corretamente.

**Possíveis causas:**
1. Gateway precisa ser reiniciado (feito, mas não resolveu)
2. Falta instalação do CLI `acpx`
3. Configuração adicional necessária

### Erro: "agentId is not allowed for sessions_spawn"

**Causa:** O sistema atual restringe `agentId` em `sessions_spawn`.

**Workaround:** Usar `runtime="acp"` com `agentId`, mas ACP não está funcionando.

---

## 🔧 Soluções Tentadas

### Tentativa 1: Configurar acp.defaultAgent
```bash
openclaw config set acp.defaultAgent "bmad-qa-bug-founder"
```
**Resultado:** Configurado, mas não resolve o erro.

### Tentativa 2: Habilitar plugin acpx
```bash
openclaw plugins enable acpx
```
**Resultado:** Plugin habilitado e carregado, mas runtime ACP não funciona.

### Tentativa 3: Reiniciar gateway
```bash
openclaw gateway restart
```
**Resultado:** Gateway reiniciado, mas ACP ainda não funciona.

---

## 📋 Próximos Passos para Correção

### Opção 1: Instalar acpx CLI
```bash
# Verificar se acpx está instalado
which acpx || npm install -g @openclaw/acpx

# Configurar no OpenClaw
openclaw config set acpx.path /usr/local/bin/acpx
```

### Opção 2: Verificar logs do gateway
```bash
tail -f /tmp/openclaw/openclaw-2026-04-07.log | grep -i acp
```

### Opção 3: Usar runtime "subagent" (alternativa)
```python
sessions_spawn(
    runtime="subagent",  # Em vez de "acp"
    mode="run",
    label="qa-agent",
    task="..."
)
```

---

## 🔄 Fluxo BMad Atual (Workaround)

Como ACP não está funcionando, estamos usando:

1. **GitHub Actions** - Simula agentes QA em paralelo
2. **Python Script** - `scripts/bmad_qa_runner.py`
3. **Makefile** - `make qa` para execução local

---

## 📊 Status Final

| Componente | Configurado | Funcionando |
|------------|-------------|-------------|
| Skills BMad | ✅ | ✅ |
| Agentes BMad | ✅ | ⚠️ Não spawnáveis |
| Plugin acpx | ✅ | ⚠️ Runtime não funciona |
| ACP Runtime | ⚠️ Parcial | ❌ Não funciona |
| Subagent spawn | ❌ | ❌ Bloqueado |

**Conclusão:** A configuração está completa, mas há limitações técnicas no ambiente atual que impedem o funcionamento correto do fluxo BMad com subagentes.
