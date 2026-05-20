# Observabilidade — Agent Swarm System

> Estratégia de observabilidade para rastrear agentes, skills, tokens e status de demandas em tempo real.

---

## Visão Geral

```
Demanda → Massuia → [Agentes] → Skills
                                    ↓
                              LangFuse SDK
                                    ↓
                         ┌──────────────────┐
                         │   LangFuse UI    │  ← Dashboard visual
                         │  (self-hosted)   │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼──────────────┐
                    ↓             ↓              ↓
               Traces         Métricas       Alertas
            (por demanda)  (tokens, tempo)  (falhas)
```

## Stack Selecionado: LangFuse (Self-Hosted)

| Critério | Decisão |
|---|---|
| **Custo** | Open-source, sem custo de licença |
| **Privacidade** | Self-hosted — dados não saem do ambiente |
| **Integração** | SDK nativo Python e Node.js |
| **LLM Support** | Qualquer provider (OpenAI, Anthropic, Ollama...) |
| **Dashboards** | Built-in por trace, sessão, usuário e modelo |

---

## O que é observado

| Evento | O que captura |
|---|---|
| `demand.received` | Tipo, origem, agente destino (Massuia) |
| `agent.started` | Agente, skill, demand_id |
| `skill.executed` | Nome da skill, input, output, duração |
| `llm.call` | Modelo, tokens (prompt + completion), custo |
| `agent.completed` | Status (success/error), tempo total |
| `escalation.triggered` | Nível, agente origem, agente destino |
| `task.status_changed` | Isa — mudança no task-board |

---

## Estrutura de Pastas

```
observability/
├── README.md                        ← este arquivo
└── langfuse/
    ├── README.md                    ← setup e quickstart
    ├── docker-compose.yml           ← stack self-hosted
    ├── .env.example                 ← variáveis necessárias
    ├── instrumentation/
    │   ├── base_agent.py            ← BaseAgent com tracing
    │   ├── skills_wrapper.py        ← @trace_skill decorator
    │   ├── demand_tracker.py        ← ciclo de vida da demanda
    │   └── token_monitor.py         ← consumo de tokens
    ├── dashboards/
    │   └── README.md                ← guia de dashboards
    └── examples/
        ├── massuia_example.py       ← supervisor com routing
        ├── marcus_example.py        ← agente dev com skills
        └── isa_example.py           ← agente ágil com métricas
```

---

## Quickstart

```bash
# 1. Subir LangFuse localmente
cd observability/langfuse
cp .env.example .env
docker compose up -d

# 2. Acessar UI
open http://localhost:3000

# 3. Copiar chaves de API da UI e adicionar ao .env
# LANGFUSE_PUBLIC_KEY=pk-lf-...
# LANGFUSE_SECRET_KEY=sk-lf-...

# 4. Instalar SDK
pip install langfuse

# 5. Instrumentar um agente
from observability.langfuse.instrumentation.base_agent import BaseAgent
```

---

## Documentos Relacionados

- [`langfuse/README.md`](./langfuse/README.md) — setup detalhado
- [`langfuse/dashboards/README.md`](./langfuse/dashboards/README.md) — dashboards e métricas
- [`../contexts/quality/task-board/README.md`](../contexts/quality/task-board/README.md) — task board da Isa
- [`../contexts/orchestration/demand-log.json`](../contexts/orchestration/demand-log.json) — log de demandas
- [`../SPEC-V2.md`](../SPEC-V2.md) — especificação do swarm
