# Tech Stack Aprovada

> Documento mantido por: **Rafa (Líder Técnico)**
> Última atualização: —

## Backend (Microserviços / Nanoserviços)

| Tipo          | Stack Aprovada                         | Observações                                       |
|---------------|----------------------------------------|---------------------------------------------------|
| API REST      | —                                      | Definir por domínio                               |
| API Async     | —                                      | Preferir brokers leves (Kafka, RabbitMQ)          |
| Runtime       | —                                      | Definir conforme linguagem do time                |
| Containerização | Docker                               | Obrigatório para todos os serviços                |
| Orquestração  | Kubernetes / Docker Compose (dev)      | K8s para produção                                 |

## Frontend

| Tipo          | Stack Aprovada                         | Observações                                       |
|---------------|----------------------------------------|---------------------------------------------------|
| SPA           | —                                      | Definir por domínio                               |

## Dados

| Tipo          | Stack Aprovada                         | Observações                                       |
|---------------|----------------------------------------|---------------------------------------------------|
| Relacional    | —                                      | Definir por domínio (ver Alexandre)                     |
| Chave-Valor   | Redis                                  | Cache e sessões                                   |
| Documento     | —                                      | Definir se necessário                             |
| Migrations    | Flyway ou Liquibase                    | Obrigatório versionamento                         |

## Qualidade e Segurança

| Ferramenta         | Finalidade                            |
|--------------------|---------------------------------------|
| Semgrep / Bandit   | SAST                                  |
| OWASP Dep-Check / Snyk | Vulnerabilidades em dependências  |
| Pact               | Contract Testing                      |
| k6 / Locust        | Performance / Load Testing            |
| Robot Framework + Python | Testes E2E                      |

## CI/CD e Infra

| Ferramenta    | Finalidade                            |
|---------------|---------------------------------------|
| GitHub Actions / GitLab CI | Pipeline CI/CD             |
| Terraform / CloudFormation | IaC                        |
| Vault / Secret Manager | Gerenciamento de secrets        |

---

> ⚠️ Qualquer alteração neste documento deve ser aprovada por Rafa e registrada em um ADR em `contexts/architecture/adr/`.
