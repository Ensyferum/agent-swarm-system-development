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
# Edite os secrets: NEXTAUTH_SECRET, SALT, ENCRYPTION_KEY, senhas

# Subir o stack
docker compose up -d

# Verificar saúde dos containers
docker compose ps
```

### Containers do Stack

| Container | Porta | Descrição |
|---|---|---|
| `langfuse-web` | `3000` | UI + API REST |
| `langfuse-worker` | `3030` (interno) | Processamento assíncrono de eventos |
| `postgres` | `5432` (localhost) | Banco de dados principal |
| `clickhouse` | `8123/9000` (localhost) | Storage de traces e eventos |
| `minio` | `9090` | Object storage S3-compatível (eventos/mídia) |
| `redis` | `6379` (localhost) | Fila de eventos entre web e worker |

> **Nota:** ClickHouse e MinIO são obrigatórios no LangFuse v3+. O Redis agora requer senha (`REDIS_AUTH`).

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
| `LANGFUSE_PUBLIC_KEY` | ✅ (SDK) | Chave pública do projeto (criada na UI) |
| `LANGFUSE_SECRET_KEY` | ✅ (SDK) | Chave secreta do projeto (criada na UI) |
| `LANGFUSE_HOST` | ✅ (SDK) | URL do servidor (ex: `http://localhost:3000`) |
| `DATABASE_URL` | ✅ (server) | PostgreSQL connection string |
| `NEXTAUTH_SECRET` | ✅ (server) | Secret para autenticação — `openssl rand -hex 32` |
| `SALT` | ✅ (server) | Salt para hashing — `openssl rand -hex 32` |
| `ENCRYPTION_KEY` | ✅ (server) | Chave 64 chars hex — `openssl rand -hex 32` |
| `CLICKHOUSE_URL` | ✅ (server) | URL HTTP do ClickHouse |
| `CLICKHOUSE_PASSWORD` | ✅ (server) | Senha do ClickHouse |
| `REDIS_AUTH` | ✅ (server) | Senha do Redis |
| `MINIO_ROOT_USER` | ✅ (server) | Usuário do MinIO |
| `MINIO_ROOT_PASSWORD` | ✅ (server) | Senha do MinIO |

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
