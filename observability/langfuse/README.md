# LangFuse — Setup e Configuração

> Plataforma open-source de LLM observability. Self-hosted via Docker Compose.

---

## Pré-requisitos

| Requisito | Versão mínima |
|---|---|
| Docker | 24+ |
| Docker Compose | 2.20+ |
| Python | 3.10+ |
| RAM disponível | 2 GB |

---

## Instalação Self-Hosted

```bash
# Clonar ou usar o docker-compose.yml deste repositório
cd observability/langfuse

# Copiar e editar variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais (ver seção abaixo)

# Subir o stack
docker compose up -d

# Verificar saúde dos containers
docker compose ps
```

### Containers do Stack

| Container | Porta | Descrição |
|---|---|---|
| `langfuse-web` | `3000` | UI + API REST |
| `langfuse-worker` | — | Processamento assíncrono de eventos |
| `postgres` | `5432` | Banco de dados principal |
| `redis` | `6379` | Fila de eventos |

---

## Configuração Inicial

1. Acesse `http://localhost:3000`
2. Crie uma conta admin
3. Crie uma **organização** (ex: `agent-swarm`)
4. Crie um **projeto** por ambiente (ex: `swarm-dev`, `swarm-prod`)
5. Vá em **Settings → API Keys** e copie:
   - `LANGFUSE_PUBLIC_KEY` (começa com `pk-lf-`)
   - `LANGFUSE_SECRET_KEY` (começa com `sk-lf-`)
6. Adicione as chaves ao `.env`

---

## Instalação do SDK Python

```bash
pip install langfuse
```

Para projetos com LangChain:

```bash
pip install langfuse langchain
```

---

## Conceitos de Rastreamento

```
Trace (1 por demanda)
└── Span: massuia.routing
└── Span: marcus.implement_feature
    └── Span: skill.create_component
        └── Generation: llm.call (tokens, modelo, latência)
└── Span: nay.review_pr
    └── Generation: llm.call
└── Span: isa.update_task_board
```

| Conceito | Descrição |
|---|---|
| **Trace** | Representa 1 demanda completa (demand_id) |
| **Span** | Uma etapa (agente ou skill) dentro do trace |
| **Generation** | Uma chamada LLM específica com métricas de token |
| **Score** | Avaliação de qualidade (manual ou automática) |
| **Session** | Agrupamento de traces relacionados |

---

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `LANGFUSE_PUBLIC_KEY` | ✅ | Chave pública do projeto |
| `LANGFUSE_SECRET_KEY` | ✅ | Chave secreta do projeto |
| `LANGFUSE_HOST` | ✅ | URL do servidor (ex: `http://localhost:3000`) |
| `DATABASE_URL` | ✅ (server) | PostgreSQL connection string |
| `REDIS_URL` | ✅ (server) | Redis connection string |
| `NEXTAUTH_SECRET` | ✅ (server) | Secret para autenticação |
| `SALT` | ✅ (server) | Salt para hashing de senhas |

---

## Atualizações

```bash
# Atualizar imagens
docker compose pull

# Reiniciar stack
docker compose up -d
```

---

## Documentação Oficial

- Site: https://langfuse.com
- GitHub: https://github.com/langfuse/langfuse
- Docs: https://langfuse.com/docs
- Self-hosting guide: https://langfuse.com/docs/deployment/self-host
