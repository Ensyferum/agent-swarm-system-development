# Padrões Arquiteturais Obrigatórios

> Documento mantido por: **Rafa (Líder Técnico)**
> Toda exceção a estes padrões deve ser registrada como débito técnico em `contexts/quality/tech-debt.md` ou justificada via ADR.

---

## Comunicação entre Serviços

- **Síncrona (REST/gRPC):** apenas quando a resposta imediata é obrigatória para o fluxo de negócio.
- **Assíncrona (mensageria):** padrão para integrações entre domínios distintos.
- **Contract First:** todo serviço deve ter contrato OpenAPI/AsyncAPI versionado antes da implementação.

## Rastreabilidade

- Todo request deve propagar um `correlationId` (header: `X-Correlation-ID`).
- Logs devem incluir sempre: `correlationId`, `serviceId`, `timestamp`, `level`, mensagem em português.
- Formato de log: JSON estruturado.

## Microserviços / Nanoserviços

- Cada serviço tem responsabilidade única e bem definida (SRP).
- Serviços não compartilham banco de dados — cada um tem seu próprio schema ou banco.
- Comunicação entre domínios sempre via API ou mensageria, nunca por acesso direto ao banco.

## Segurança

- Autenticação via JWT ou OAuth2 (definir por domínio).
- Secrets nunca em código ou repositório; sempre via gerenciador (Vault, Secret Manager).
- Todo endpoint autenticado; princípio de menor privilégio.

## Dados e Persistência

- Migrations obrigatórias e versionadas (up/down).
- Schemas respeitam bounded contexts (`contexts/domain/bounded-contexts.md`).
- Queries devem ter plano de execução validado por Alexandre para tabelas com alto volume.

## Código

- Sem boilerplates; código mínimo e nomenclatura intuitiva.
- Cobertura mínima de testes: **80%** em branches críticas.
- Complexidade ciclomática máxima por método: **10**.
- Nenhuma dependência direta entre módulos de domínios distintos.

## Entrega

- Toda feature via Pull Request com review aprovado por Nay e Rafa.
- Branching strategy definida em `contexts/orchestration/branching-strategy.md`.
- Definition of Done em `contexts/quality/definition-of-done.md`.
