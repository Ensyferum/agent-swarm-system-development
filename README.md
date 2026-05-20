# 🤖 Agent Swarm System — Development

> Ecossistema autônomo de agentes especializados para condução do ciclo completo de desenvolvimento de software — da demanda ao deploy em produção — com supervisão humana nos gates críticos.

---

## Visão Geral

O **Agent Swarm** é uma estrutura de múltiplos agentes de IA que colaboram para executar o ciclo completo de desenvolvimento: refinamento de negócio, arquitetura, implementação, revisão, segurança, testes e deploy.

Cada agente tem uma especialidade, um conjunto de skills e um conjunto de documentos de contexto que consulta como **fonte primária de verdade** antes de agir — o **Princípio Document-First**.

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

## 👥 Agentes

| Codinome | Papel | Especialidade |
|----------|-------|---------------|
| **Massuia** | Supervisor | Ponto de entrada único. Recebe, classifica e orquestra toda demanda |
| **Isa** | Controle Ágil | Task board global, métricas, impedimentos e release notes |
| **Manu** | Product Owner | Regras de negócio, critérios de aceite e histórias em BDD |
| **Rafa** | Líder Técnico | Decisões arquiteturais, CodeMap, distribuição de tasks técnicas |
| **Marcus** | Desenvolvedor | Implementação, scaffolding, build e testes locais |
| **Alexandre** | DBA / Arq. de Dados | Schemas, migrations e modelagem de dados por domínio |
| **Nay** | Reviewer | Code review formal e independente antes do merge |
| **Erick** | SecOps | SAST, DAST, secret scanning e políticas de segurança |
| **Dani** | QA | Testes BDD, E2E, contrato e performance |
| **Eric** | DevOps / SRE | CI/CD, infraestrutura como código e deploy |

---

## 🔄 Fluxos por Tipo de Demanda

| Tipo | Sequência |
|------|-----------|
| **Feature nova** | Massuia → Manu → Rafa → Alexandre → Marcus → Nay → Erick → Dani → Eric → Erick(DAST) |
| **Bug funcional** | Massuia → Manu → Rafa → Marcus → Nay → Erick → Dani → Eric |
| **Hotfix** | Massuia → Rafa → Marcus → Erick → Eric |
| **Refactor** | Massuia → Rafa → Marcus → Nay → Erick → Dani → Eric |
| **Infra / Pipeline** | Massuia → Rafa → Eric → Erick |
| **Security fix** | Massuia → Erick → Marcus → Nay → Eric |
| **Spike / Research** | Massuia → Rafa (→ Marcus se necessário) |

> **Isa** monitora todos os fluxos de forma contínua e assíncrona.

---

## 🛠️ Skills (34 no total)

| Skill | Agente |
|-------|--------|
| `classify-demand` · `consolidate-report` · `generate-agent` · `generate-skill` | Massuia |
| `gerar-relatorio-progresso` · `gerar-relatorio-impedimentos` · `atualizar-quadro-tarefas` · `gerar-release-notes` · `gerar-metricas-ageis` | Isa |
| `scaffolding` · `padronizacao-commits` · `padronizacao-pull-requests` · `validate-api-contract` · `security-pre-commit-hook` | Marcus |
| `scaffolding-qa` · `bdd-to-test` · `contract-testing` · `performance-testing` | Dani |
| `bdd-story-writer` · `generate-po-brief` | Manu |
| `codemap-mapper` · `generate-task-brief` · `generate-impact-map` · `summarize-adr` | Rafa |
| `analyze-diff` · `generate-critical-tests` | Nay |
| `scaffolding-pipeline` · `iac-generator` · `deploy-canary-rollback` | Eric |
| `sast-scan` · `dependency-vulnerability-check` · `secret-scanning` | Erick |
| `scaffolding-migrations` · `domain-data-modeling` · `query-plan-analyzer` | Alexandre |

> Catálogo completo com finalidades: [`SPEC-V2.md — Seção 10`](./SPEC-V2.md)

---

## 📁 Estrutura de Contextos

> Todo agente consulta os documentos de `contexts/` como **fonte primária** antes de agir.
> Cada agente carrega apenas os documentos relevantes à sua execução — evitando desperdício de contexto.

```
contexts/
├── architecture/
│   ├── adr/                    # Architecture Decision Records
│   ├── tech-stack.md           # Stack aprovada por tipo de serviço
│   └── patterns.md             # Padrões arquiteturais obrigatórios
├── domain/
│   ├── glossary.md             # Vocabulário de domínio
│   └── bounded-contexts.md     # Bounded contexts e regras de integração
├── services/
│   ├── registry.json           # Catálogo de serviços
│   └── codemap/                # CodeMap detalhado por serviço
├── quality/
│   ├── definition-of-done.md   # Critérios de DoD
│   ├── tech-debt.md            # Débitos técnicos
│   ├── task-board/             # Task board global (Isa)
│   └── test-repository/        # Testes reutilizáveis (Dani)
├── security/
│   └── policies.md             # Políticas de segurança (Erick)
└── orchestration/
    ├── demand-log.json          # Log de demandas (Massuia)
    ├── escalation-protocol.md   # Protocolo de escalação por nível
    └── branching-strategy.md    # Git branching strategy e commits
```

| Contexto | Responsável | Quem usa |
|----------|-------------|----------|
| `architecture/` | Rafa | Marcus, Nay, Rafa |
| `domain/` | Manu + Alexandre | Dani, Manu, Alexandre, Rafa |
| `services/` | Rafa + Eric | Rafa, Eric, Nay |
| `quality/` | Rafa + Dani + Isa | Todos |
| `security/` | Erick | Erick, Nay, Eric, Marcus |
| `orchestration/` | Massuia + Rafa | Massuia, Marcus, Isa |

---

## 📐 Princípio Document-First

> **Todo agente deve, primariamente, basear suas ações nos documentos já gerados em `contexts/`.**

1. O agente carrega **somente os docs do seu Mapa de Contextos** antes de executar
2. Nunca assume informação que não esteja nos documentos ou na task recebida
3. Em caso de conflito entre instrução e documento → **para e escala** (`escalation-protocol.md`)
4. O SPEC é o **índice**; os documentos são a **fonte de verdade**

---

## 🔀 Branching Strategy

```
<tipo>/<dominio>/<descricao-curta>
```

| Branch | Finalidade |
|--------|------------|
| `main` | Produção — protegida, somente via PR |
| `develop` | Homologação — protegida, somente via PR |
| `feature/<dominio>/<desc>` | Nova funcionalidade |
| `fix/<dominio>/<desc>` | Correção de bug |
| `refactor/<dominio>/<desc>` | Refatoração |
| `hotfix/<desc>` | Correção urgente em produção |
| `docs/<desc>` | Documentação |
| `security/<desc>` | Correção de segurança |

**Formato de commit:**
```
<tipo>(<escopo>): <mensagem no imperativo em português>

feat(pagamentos): adiciona endpoint de estorno com validação de prazo
fix(auth): corrige expiração incorreta do refresh token
```

> Detalhes completos: [`contexts/orchestration/branching-strategy.md`](./contexts/orchestration/branching-strategy.md)

---

## ✅ Definition of Done

Uma entrega é **concluída** somente quando:

1. ✅ Código implementado + testes unitários passando (≥ 80% cobertura)
2. ✅ Schema e migrations validados por Alexandre *(se aplicável)*
3. ✅ Code review aprovado por Nay
4. ✅ SAST e secret scan aprovados por Erick
5. ✅ Testes BDD, E2E e contrato aprovados por Dani
6. ✅ Pipeline CI/CD passando em homolog + deploy validado por Eric
7. ✅ DAST aprovado por Erick em homolog
8. ✅ PR documentado e aprovado por Nay + Rafa
9. ✅ CodeMap e ADRs atualizados por Rafa
10. ✅ Relatório consolidado emitido por Massuia
11. ✅ **Aprovação humana recebida**

> Critérios por tipo de entrega: [`contexts/quality/definition-of-done.md`](./contexts/quality/definition-of-done.md)

---

## 📄 Documentação

| Documento | Descrição |
|-----------|-----------|
| [`SPEC-V2.md`](./SPEC-V2.md) | Especificação completa v2.1 — agentes, skills, fluxos e contextos |
| [`SPEC.md`](./SPEC.md) | Especificação original v1 |
| [`contexts/`](./contexts/) | Base documental completa do swarm |
