# Registro de Débitos Técnicos

> Mantido por: **Rafa (Líder Técnico)**
> Todo agente que identifica um débito técnico deve registrá-lo aqui via PR ou diretamente durante a execução.

---

## Classificação de Severidade

| Severidade | Critério                                                            | SLA para resolução      |
|------------|---------------------------------------------------------------------|------------------------|
| 🔴 Crítico  | Risco de segurança, falha de dados ou bloqueio de produção          | Próximo ciclo obrigatório |
| 🟠 Alto     | Impacta performance, escalabilidade ou manutenibilidade relevante   | Até 2 ciclos             |
| 🟡 Médio    | Viola padrões mas sem impacto imediato                              | Até 4 ciclos             |
| 🟢 Baixo    | Melhorias desejáveis, sem impacto funcional                         | Backlog                  |

---

## Débitos Registrados

| ID    | Severidade | Serviço / Módulo | Descrição                         | Identificado por | Data       | Status     | Resolução |
|-------|------------|------------------|-----------------------------------|------------------|------------|------------|-----------|
| —     | —          | —                | —                                 | —                | —          | —          | —         |

---

## Como Registrar

```markdown
| DT-001 | 🟠 Alto | pagamentos-service | Query N+1 no endpoint de listagem | Nay (Reviewer) | 2026-05-20 | Pendente | — |
```

## Status Possíveis

- `Pendente` — identificado, aguardando priorização
- `Em andamento` — sendo resolvido no ciclo atual
- `Resolvido` — corrigido, vincular ao PR/commit
- `Aceito` — débito aceito conscientemente (registrar motivo)
- `Descartado` — irrelevante após reavaliação (registrar motivo)
