# Definition of Done (DoD)

> Aprovado por: **Rafa (Líder Técnico)** + **Manu (Product Owner)**
> Uma entrega **só é considerada concluída** quando **todos** os critérios abaixo são atendidos.

---

## Critérios Obrigatórios

### 1. Implementação (Marcus)
- [ ] Código implementado seguindo os padrões de `contexts/architecture/patterns.md`
- [ ] Todos os testes unitários passando (cobertura mínima: 80%)
- [ ] `correlationId` propagado em todos os pontos de entrada e saída
- [ ] Logs em português, formato JSON estruturado
- [ ] Nenhum secret ou credencial em código ou variável hardcoded
- [ ] Contrato OpenAPI/AsyncAPI atualizado (se aplicável)
- [ ] Commits seguindo o padrão definido em `contexts/orchestration/branching-strategy.md`

### 2. Contrato e Dados (Alexandre — se aplicável)
- [ ] Schema de banco de dados definido e documentado
- [ ] Migrations versionadas com up/down funcionais
- [ ] Plano de execução de queries críticas validado

### 3. Code Review (Nay)
- [ ] Review formal realizado via skill `analyze-diff`
- [ ] Nenhum bloqueio crítico pendente
- [ ] Aderência ao CodeMap e ADRs verificada

### 4. Segurança (Erick)
- [ ] SAST executado sem issues críticos ou altos
- [ ] Dependências sem CVEs críticos conhecidos
- [ ] Nenhum secret detectado no repositório

### 5. Qualidade (Dani)
- [ ] Cenários BDD implementados e passando
- [ ] Testes E2E executados e aprovados
- [ ] Testes de contrato passando (se houver integração com outros serviços)
- [ ] Dados no banco validados conforme regras de negócio

### 6. Entrega
- [ ] Pull Request documentado: descrição, critérios de aceite, link para história
- [ ] PR aprovado por Nay (Reviewer) e Rafa (Líder Técnico)
- [ ] Pipeline CI/CD passando em ambiente de homologação
- [ ] Deploy em homologação validado por Eric (DevOps)

### 7. Documentação e Rastreabilidade
- [ ] CodeMap atualizado por Rafa
- [ ] ADR criado se houver decisão arquitetural relevante
- [ ] Débitos técnicos identificados registrados em `contexts/quality/tech-debt.md`

### 8. Validação Humana
- [ ] Relatório de execução emitido por todos os agentes envolvidos
- [ ] Aprovação humana recebida antes do merge em `main`

---

## Critérios por Tipo de Entrega

| Tipo de Entrega     | Critérios obrigatórios               | Critérios dispensáveis          |
|---------------------|--------------------------------------|----------------------------------|
| Nova feature        | Todos                                | —                                |
| Bugfix              | 1, 3, 4, 6, 8                        | 2 (se não há mudança de schema)  |
| Refactor            | 1, 3, 4, 5 (regressão), 6, 7, 8     | 2                                |
| Infra/Pipeline      | 4, 6, 8                              | 2, 5                             |
| Hotfix              | 1, 4, 8                              | Demais (compensar no próximo ciclo) |
