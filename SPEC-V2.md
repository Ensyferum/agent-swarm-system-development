# Agent Swarm System — SPEC v2.1

> **Versão:** 2.1 | **Data:** 2026-05-20 | **Status:** Ativo

---

## 1. Visão Geral

Ecossistema autônomo de agentes especializados para condução do ciclo completo de desenvolvimento de software — da demanda ao deploy em produção — com supervisão humana nos gates críticos.

---

## 2. Princípio Document-First

> **Todo agente deve, primariamente, basear suas ações nos documentos já gerados em `contexts/`.**

- Antes de qualquer execução, o agente **carrega os documentos listados no seu Mapa de Contextos** (Seção 6)
- O agente **nunca assume** informação que não esteja nos documentos carregados ou na task recebida
- Em caso de conflito entre instrução recebida e documento de contexto, o agente **para e escala** (ver `orchestration/escalation-protocol.md`)
- **O SPEC é o índice; os documentos em `contexts/` são a fonte de verdade**
- Skills carregam seu próprio contexto mínimo — o agente não precisa repassar o que a skill já sabe

---

## 3. Arquitetura

```
[Humano] ──► MASSUIA (Supervisor)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
      MANU                 ISA ◄─── monitora tudo (assíncrono)
      (PO)               (Agile)
        │                   │
        ▼                   │
      RAFA   ◄──────────────┘
      (TL)
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
MARCUS ALEXANDRE   ERIC
 (Dev)  (DBA)     (DevOps)
   │                   │
   ▼                   │
 NAY ──► ERICK ──► DANI│  ◄── pipeline de qualidade
   └───────────────────┘
             │
       [Gate Humano]
             │
       [Merge / Deploy]
```

---

## 4. Regras Gerais

| # | Regra |
|---|-------|
| 1 | **Document-First:** Agentes baseiam ações nos docs de `contexts/` como fonte primária — nunca reinventam o que já está documentado |
| 2 | **Task tracking:** Notificar Isa e atualizar estado individual antes e após cada execução |
| 3 | **Task board global:** Gerenciado por Isa; agentes avançam ou recuam conforme o estado da task |
| 4 | **Relatório obrigatório:** Emitir relatório estruturado ao final de cada execução |
| 5 | **Padrão Copilot:** Agentes e Skills escritos no padrão Copilot |
| 6 | **Geração de artefatos:** Skills via `generate-skill`; Agentes via `generate-agent` |
| 7 | **Gates humanos:** Swarm pausa para aprovação nos pontos definidos em `quality/definition-of-done.md` |

---

## 5. Agentes

> **Formato por agente:** papel resumido · documentos primários a carregar · skills · fluxo de comunicação.
> Regras detalhadas estão nos documentos de contexto referenciados — não são repetidas aqui.

---

### 5.1 Massuia — Supervisor

**Papel:** Ponto de entrada único. Recebe, classifica e orquestra toda demanda. Não toma decisões técnicas.
**Docs primários:** `orchestration/demand-log.json` · `orchestration/escalation-protocol.md`
**Skills:** `classify-demand` · `consolidate-report` · `generate-agent` · `generate-skill`
**Reporta a:** Humano · **Aciona:** Manu, Rafa, Isa

---

### 5.2 Isa — Controle Ágil

**Papel:** Guardiã do estado do projeto. Monitora tasks, detecta impedimentos e gera métricas ágeis. Nunca bloqueia outros agentes.
**Docs primários:** `quality/task-board/README.md`
**Skills:** `gerar-relatorio-progresso` · `gerar-relatorio-impedimentos` · `atualizar-quadro-tarefas` · `gerar-release-notes` · `gerar-metricas-ageis`
**Reporta a:** Massuia · **Monitora:** todos os agentes (assíncrono)

---

### 5.3 Marcus — Desenvolvedor

**Papel:** Implementação de código, scaffolding, build e testes locais.
**Docs primários:** `architecture/patterns.md` · `architecture/tech-stack.md` · `orchestration/branching-strategy.md` · task-brief da task atual
**Skills:** `scaffolding` · `padronizacao-commits` · `padronizacao-pull-requests` · `validate-api-contract` · `security-pre-commit-hook`
**Reporta a:** Rafa · **Notifica:** Isa

---

### 5.4 Dani — QA

**Papel:** Valida integridade funcional, regras de negócio e critérios de aceite.
**Docs primários:** `quality/test-repository/README.md` · `domain/bounded-contexts.md` · BDD stories da feature atual
**Skills:** `scaffolding-qa` · `bdd-to-test` · `contract-testing` · `performance-testing`
**Reporta a:** Massuia · **Notifica:** Isa

---

### 5.5 Manu — Product Owner

**Papel:** Detentora de regras de negócio e critérios de aceite. Escreve histórias em BDD.
**Docs primários:** `domain/glossary.md` · `domain/bounded-contexts.md` · histórias existentes do produto
**Skills:** `bdd-story-writer` · `generate-po-brief`
**Reporta a:** Massuia · **Notifica:** Isa

---

### 5.6 Rafa — Líder Técnico

**Papel:** Decisões técnicas e arquiteturais. Distribui tasks entre os agentes de execução.
**Docs primários:** `services/registry.json` · `services/codemap/` · `architecture/patterns.md` · `architecture/tech-stack.md` · `architecture/adr/` · `quality/tech-debt.md`
**Skills:** `codemap-mapper` · `generate-task-brief` · `generate-impact-map` · `summarize-adr`
**Reporta a:** Massuia · **Distribui para:** Marcus, Alexandre, Eric · **Notifica:** Isa

---

### 5.7 Nay — Reviewer

**Papel:** Code review formal e independente antes do merge. Nunca revisa código que implementou.
**Docs primários:** `architecture/patterns.md` · `security/policies.md` · `services/codemap/` (serviço em revisão) · diff do PR atual
**Skills:** `analyze-diff` · `generate-critical-tests`
**Reporta a:** Rafa · **Notifica:** Isa

---

### 5.8 Eric — DevOps / SRE

**Papel:** Infraestrutura, CI/CD, ambientes e deploy.
**Docs primários:** `services/registry.json` · `security/policies.md` · IaC do serviço em deploy
**Skills:** `scaffolding-pipeline` · `iac-generator` · `deploy-canary-rollback`
**Reporta a:** Massuia · **Notifica:** Isa

---

### 5.9 Erick — SecOps

**Papel:** Segurança preventiva (SAST/secrets pré-merge) e reativa (DAST pós-deploy em homolog). Bloqueia o fluxo em issues críticos ou altos.
**Docs primários:** `security/policies.md` · diff do PR atual (SAST) ou URL de homolog (DAST)
**Skills:** `sast-scan` · `dependency-vulnerability-check` · `secret-scanning`
**Reporta a:** Massuia · **Bloqueia fluxo se:** issues críticos/altos · **Notifica:** Isa

---

### 5.10 Alexandre — DBA / Arquiteto de Dados

**Papel:** Estratégia de dados — schemas, migrations, modelagem por domínio.
**Docs primários:** `domain/bounded-contexts.md` · `domain/glossary.md` · schemas existentes do domínio
**Skills:** `scaffolding-migrations` · `domain-data-modeling` · `query-plan-analyzer`
**Reporta a:** Rafa · **Notifica:** Isa

---

## 6. Mapa de Contextos por Agente

> Cada agente carrega **somente** os documentos desta tabela — nada além, a menos que a task específica exija.
> Carregar contexto desnecessário desperdiça tokens e aumenta risco de conflito de instruções.

| Agente      | Documentos a carregar no início da execução                                           |
|-------------|----------------------------------------------------------------------------------------|
| Massuia     | `orchestration/demand-log.json` · `orchestration/escalation-protocol.md`              |
| Isa         | `quality/task-board/README.md`                                                         |
| Marcus      | `architecture/patterns.md` · `architecture/tech-stack.md` · `orchestration/branching-strategy.md` · task-brief (task atual) |
| Dani        | `quality/test-repository/README.md` · `domain/bounded-contexts.md` · BDD stories (feature atual) |
| Manu        | `domain/glossary.md` · `domain/bounded-contexts.md`                                   |
| Rafa        | `services/registry.json` · `services/codemap/` · `architecture/patterns.md` · `architecture/tech-stack.md` · `architecture/adr/` · `quality/tech-debt.md` |
| Nay         | `architecture/patterns.md` · `security/policies.md` · `services/codemap/` (serviço) · diff (PR atual) |
| Eric        | `services/registry.json` · `security/policies.md` · IaC do serviço                    |
| Erick       | `security/policies.md` · diff do PR (SAST) ou URL homolog (DAST)                      |
| Alexandre   | `domain/bounded-contexts.md` · `domain/glossary.md` · schemas do domínio              |

---

## 7. Fluxos por Tipo de Demanda

| Tipo              | Sequência de agentes                                                   | Gate humano |
|-------------------|------------------------------------------------------------------------|-------------|
| Feature nova      | Massuia→Manu→Rafa→Alexandre→Marcus→Nay→Erick→Dani→Eric→Erick(DAST)   | Sim         |
| Bug funcional     | Massuia→Manu→Rafa→Marcus→Nay→Erick→Dani→Eric                          | Sim         |
| Hotfix            | Massuia→Rafa→Marcus→Erick→Eric                                         | Sim (rápido)|
| Refactor          | Massuia→Rafa→Marcus→Nay→Erick→Dani(regressão)→Eric                    | Sim         |
| Infra / Pipeline  | Massuia→Rafa→Eric→Erick                                                | Sim         |
| Security fix      | Massuia→Erick→Marcus→Nay→Eric                                          | Sim (urgente)|
| Spike / Research  | Massuia→Rafa (→Marcus se necessário)                                   | Não         |

> **Isa** monitora todos os fluxos de forma contínua e assíncrona.

---

## 8. Orquestração

> Toda regra de orquestração vive exclusivamente nos documentos abaixo. Não há resumo inline — carregue o doc.

| Regra                  | Documento                                        |
|------------------------|--------------------------------------------------|
| Escalation Protocol    | `contexts/orchestration/escalation-protocol.md`  |
| Branching Strategy     | `contexts/orchestration/branching-strategy.md`   |
| Definition of Done     | `contexts/quality/definition-of-done.md`         |
| Políticas de Segurança | `contexts/security/policies.md`                  |
| Padrões Arquiteturais  | `contexts/architecture/patterns.md`              |
| Stack Aprovada         | `contexts/architecture/tech-stack.md`            |

---

## 9. Estrutura de Contextos

```
contexts/
├── architecture/
│   ├── adr/                    # ADRs — decisões arquiteturais (Rafa)
│   ├── tech-stack.md           # Stack aprovada por tipo de serviço
│   └── patterns.md             # Padrões arquiteturais obrigatórios
├── domain/
│   ├── glossary.md             # Vocabulário de domínio (Manu + Alexandre)
│   └── bounded-contexts.md     # Bounded contexts e regras de integração
├── services/
│   ├── registry.json           # Catálogo de serviços — versão, stack, status (Rafa + Eric)
│   └── codemap/                # CodeMap detalhado por serviço (Rafa)
├── quality/
│   ├── definition-of-done.md   # Critérios completos de DoD
│   ├── tech-debt.md            # Débitos técnicos registrados
│   ├── task-board/             # Task board global (Isa)
│   └── test-repository/        # Testes BDD, E2E, contrato e performance reutilizáveis (Dani)
├── security/
│   └── policies.md             # Políticas de segurança obrigatórias (Erick)
└── orchestration/
    ├── demand-log.json          # Log de demandas recebidas (Massuia)
    ├── escalation-protocol.md   # Protocolo de escalação por nível
    └── branching-strategy.md    # Git branching strategy e padrão de commits
```

| Contexto        | Responsável (escrita)   | Acesso  |
|-----------------|-------------------------|---------|
| architecture/   | Rafa                    | Todos   |
| domain/         | Manu + Alexandre        | Todos   |
| services/       | Rafa + Eric             | Todos   |
| quality/        | Rafa + Dani + Isa       | Todos   |
| security/       | Erick                   | Todos   |
| orchestration/  | Massuia + Rafa          | Todos   |

---

## 10. Catálogo de Skills

| Skill                              | Agente     | Finalidade                                              |
|------------------------------------|------------|---------------------------------------------------------|
| `classify-demand`                  | Massuia    | Classificar tipo, urgência e impacto da demanda         |
| `consolidate-report`               | Massuia    | Consolidar relatórios de agentes em visão executiva     |
| `generate-agent`                   | Massuia    | Gerar novos agentes no padrão Copilot                   |
| `generate-skill`                   | Massuia    | Gerar novas skills no padrão Copilot                    |
| `gerar-relatorio-progresso`        | Isa        | Burndown, velocity e status do ciclo atual              |
| `gerar-relatorio-impedimentos`     | Isa        | Bloqueios e escalações com SLA de resolução             |
| `atualizar-quadro-tarefas`         | Isa        | Sincronizar task board global                           |
| `gerar-release-notes`              | Isa        | Release notes por commits, PRs e tasks concluídas       |
| `gerar-metricas-ageis`             | Isa        | Throughput, lead time, cycle time                       |
| `scaffolding`                      | Marcus     | Geração de projetos                                     |
| `padronizacao-commits`             | Marcus     | Commits no padrão definido                              |
| `padronizacao-pull-requests`       | Marcus     | PRs com template completo                               |
| `validate-api-contract`            | Marcus     | Geração e validação de contratos OpenAPI/AsyncAPI       |
| `security-pre-commit-hook`         | Marcus     | Verificação de secrets e lint de segurança pré-commit   |
| `scaffolding-qa`                   | Dani       | Geração de projetos de teste por domínio                |
| `bdd-to-test`                      | Dani       | Cenários BDD → casos de teste executáveis               |
| `contract-testing`                 | Dani       | Testes de contrato entre serviços via Pact              |
| `performance-testing`              | Dani       | Testes de carga com k6/Locust                           |
| `bdd-story-writer`                 | Manu       | Escrita de histórias no formato BDD                     |
| `generate-po-brief`                | Manu       | Regras de negócio e critérios de aceite funcionais      |
| `codemap-mapper`                   | Rafa       | Mapeamento e atualização do CodeMap de serviços         |
| `generate-task-brief`              | Rafa       | Task técnica estruturada com escopo, riscos e critérios |
| `generate-impact-map`              | Rafa       | Mapa de impacto técnico de uma tarefa                   |
| `summarize-adr`                    | Rafa       | Criar e consolidar Architecture Decision Records        |
| `analyze-diff`                     | Nay        | Review estruturado: segurança, arquitetura, regressão   |
| `generate-critical-tests`          | Nay        | Verificação de cobertura dos cenários críticos          |
| `scaffolding-pipeline`             | Eric       | Geração de pipelines CI/CD                              |
| `iac-generator`                    | Eric       | Infrastructure as Code (Terraform/CloudFormation)       |
| `deploy-canary-rollback`           | Eric       | Deploy canário com rollback automatizado                |
| `sast-scan`                        | Erick      | Análise estática de segurança (Semgrep, Bandit)         |
| `dependency-vulnerability-check`   | Erick      | CVEs em dependências (Snyk, OWASP Dep-Check)            |
| `secret-scanning`                  | Erick      | Detecção de secrets e credenciais expostas              |
| `scaffolding-migrations`           | Alexandre  | Migrations versionadas com Flyway/Liquibase             |
| `domain-data-modeling`             | Alexandre  | Modelagem de dados por domínio de negócio               |
| `query-plan-analyzer`              | Alexandre  | Análise de plano de execução de queries críticas        |