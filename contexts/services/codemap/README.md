# CodeMap — Mapa de Serviços

> Mantido por: **Rafa (Líder Técnico)** via skill `Mapeador de Codemap`
> Gerado e atualizado a cada novo serviço criado ou modificado.

---

## Estrutura de um CodeMap por Serviço

Cada serviço deve ter seu próprio arquivo `<nome-do-servico>.md` nesta pasta com a seguinte estrutura:

```markdown
# CodeMap: <nome-do-servico>

**Domínio:** <bounded context>
**Responsável:** Marcus (última entrega) | Rafa (arquitetura)
**Stack:** <linguagem, framework, banco>
**Repositório:** <url>
**Versão atual:** <semver>

## Endpoints / Eventos

| Método | Path / Tópico     | Contrato                  | Autenticação |
|--------|-------------------|---------------------------|-------------|
| GET    | /exemplo          | openapi/exemplo.yaml      | JWT         |

## Dependências

| Serviço / Recurso | Tipo de Integração | Contrato            |
|-------------------|--------------------|---------------------|
| —                 | —                  | —                   |

## Modelo de Dados

Ver: `contexts/domain/<dominio>/schema.md`

## Débitos Técnicos

Ver: `contexts/quality/tech-debt.md` — filtrar por `serviceId: <nome>`

## Histórico de ADRs Aplicadas

| ADR    | Decisão resumida               |
|--------|-------------------------------|
| —      | —                             |
```

---

## Índice de Serviços

| Serviço | Domínio | Linguagem | Status |
|---------|---------|-----------|--------|
| —       | —       | —         | —      |
