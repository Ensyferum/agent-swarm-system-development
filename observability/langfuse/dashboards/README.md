# LangFuse — Dashboards e Métricas

> Guia de configuração dos dashboards de observabilidade do Agent Swarm.

---

## Acesso à UI

```
http://localhost:3000
```

Após fazer login, selecione o projeto `swarm-dev` (ou o ambiente configurado).

---

## Seções da UI do LangFuse

### 1. Traces

Visão individual por demanda — cada `demand_id` é um trace completo.

**O que ver:**
- Timeline de spans: `massuia.routing → marcus.execute → nay.review_pr`
- Duração de cada etapa
- Input/output de cada span
- Chamadas LLM com tokens e modelo

**Filtros úteis:**
- `tags = "feature"` — apenas demandas de feature
- `tags = "marcus"` — todas as execuções do Marcus
- `metadata.final_status = "error"` — demandas com falha

---

### 2. Sessions

Agrupa traces relacionados (ex: uma sprint completa, ou uma issue com sub-tasks).

**Configuração recomendada:** usar `demand_id` como `session_id` para manter
a rastreabilidade de demandas com múltiplas iterações.

---

### 3. Generations (Chamadas LLM)

Tabela de todas as chamadas LLM com métricas consolidadas.

**Métricas disponíveis:**
| Coluna | Descrição |
|---|---|
| Model | Modelo usado (gpt-4o, claude-3-5-sonnet...) |
| Prompt Tokens | Tokens enviados |
| Completion Tokens | Tokens recebidos |
| Total Tokens | Soma |
| Latency | Tempo de resposta do modelo |
| Cost | Custo estimado (se modelo configurado) |

**Filtros úteis:**
- `metadata.agent = "marcus"` — tokens consumidos pelo Marcus
- `metadata.skill = "generate_tests"` — custo da skill de testes

---

### 4. Dashboard de Métricas (Analytics)

Gráficos automáticos disponíveis na aba **Analytics**:

```
┌─────────────────────────────────────────────────────┐
│  Tokens por dia          │  Latência média por agente │
│  ▓▓▓▓░░▓▓▓░░░           │  massuia  ▓░░░ 1.2s        │
│                          │  marcus   ▓▓▓▓ 8.4s        │
│                          │  nay      ▓▓░░ 4.1s        │
├─────────────────────────────────────────────────────┤
│  Demandas por status     │  Top skills por token      │
│  ✅ success: 78%         │  1. implement_feature 45%  │
│  ❌ error:   12%         │  2. generate_tests    22%  │
│  ⚠️  escalation: 10%    │  3. review_pr         18%  │
└─────────────────────────────────────────────────────┘
```

---

## Métricas-Chave por Agente

| Agente | Métrica Principal | Alerta Sugerido |
|---|---|---|
| **Massuia** | Tempo de routing | > 5s → revisar classificação |
| **Marcus** | Tokens por feature | > 8k tokens → prompt muito verboso |
| **Eric** | Duração de pipeline | > 15min → investigar infra |
| **Alexandre** | Tokens por schema | > 5k tokens → schema muito complexo |
| **Nay** | Taxa de aprovação | < 70% → qualidade de código baixa |
| **Erick** | Bloqueios de segurança | > 2/semana → rever políticas |
| **Rafa** | Decisões técnicas/sprint | — |
| **Isa** | Cycle time médio | > SLA → escalar para Massuia |
| **Manu** | Tokens por doc | > 3k → doc muito longa |
| **Dani** | Falhas de teste | > 10% → rever suite |

---

## Configurar Alertas (via Webhook)

LangFuse suporta alertas via webhook na versão Cloud. No self-hosted,
configure um script que consulte a API periodicamente:

```bash
# Verificar traces com erro nas últimas 1h
curl -s "http://localhost:3000/api/public/traces" \
  -H "Authorization: Basic $(echo -n pk-lf-...:sk-lf-... | base64)" \
  -G -d "filter=metadata.final_status%3Derror" \
  -d "fromTimestamp=$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)"
```

---

## Scores — Avaliação de Qualidade

Adicione scores manuais ou automáticos aos traces para medir qualidade:

```python
langfuse.score(
    trace_id=demand_id,
    name="code_quality",
    value=0.85,          # 0.0 a 1.0
    comment="PR aprovado com 2 comentários menores"
)
```

**Scores recomendados:**
| Score | Quem atribui | Critério |
|---|---|---|
| `code_quality` | Nay | Resultado do review |
| `test_coverage` | Dani | Cobertura de testes |
| `security_check` | Erick | Resultado da análise |
| `routing_accuracy` | Massuia | Agente correto acionado? |

---

## Exportar Dados

```bash
# Exportar traces como CSV (via API)
curl "http://localhost:3000/api/public/traces?limit=100&format=csv" \
  -H "Authorization: Basic ..."

# Ou via SDK Python
from langfuse import Langfuse
lf = Langfuse(...)
traces = lf.get_traces(limit=100)
```
