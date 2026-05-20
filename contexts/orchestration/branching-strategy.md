# Branching Strategy

> Mantido por: **Rafa (Líder Técnico)**
> Aplicado por: **Marcus (Desenvolvedor)**, **Eric (DevOps)**
> Todos os agentes que interagem com Git devem seguir estas convenções.

---

## Branches Principais (Protegidas)

| Branch    | Finalidade                            | Acesso direto |
|-----------|---------------------------------------|---------------|
| `main`    | Produção — código estável e deployado | ❌ Proibido   |
| `develop` | Integração — homologação contínua     | ❌ Proibido   |

> ⚠️ Nunca realizar commits diretos em `main` ou `develop`. **Sempre via Pull Request.**

---

## Branches de Trabalho

### Nomenclatura

```
<tipo>/<dominio>/<descricao-curta>
```

| Tipo        | Uso                                             | Exemplo                                    |
|-------------|--------------------------------------------------|--------------------------------------------|
| `feature`   | Nova funcionalidade                              | `feature/pagamentos/endpoint-estorno`      |
| `fix`       | Correção de bug                                  | `fix/autenticacao/refresh-token-expirado`  |
| `refactor`  | Refatoração sem mudança de comportamento         | `refactor/pedidos/simplificar-service`     |
| `infra`     | Mudanças de infraestrutura ou pipeline           | `infra/adicionar-stage-sast`               |
| `security`  | Correção de vulnerabilidade de segurança         | `security/atualizar-dependencia-jwt`       |
| `docs`      | Documentação técnica ou de contexto              | `docs/codemap-pagamentos`                  |
| `test`      | Adição ou correção de testes                     | `test/pagamentos/contract-test-provedor`   |
| `hotfix`    | Correção urgente em produção                     | `hotfix/pagamentos/calculo-taxa-errado`    |

### Regras
- Descrição sempre em **kebab-case** e em **português ou inglês** (manter consistência por projeto)
- Branches `hotfix/*` são criadas a partir de `main` e mergeadas em `main` e `develop`
- Todas as demais branches partem de `develop`
- Branches devem ser deletadas após merge aprovado

---

## Pull Requests

### Obrigatório em todo PR

1. **Título:** `[tipo] dominio: descrição clara` — ex: `[feature] pagamentos: adicionar endpoint de estorno`
2. **Descrição:** o que foi feito, por que, e link para a história/task de origem
3. **Critérios de aceite:** listados e verificados
4. **Checklist de DoD:** referência a `contexts/quality/definition-of-done.md`

### Aprovações necessárias

| Branch destino | Aprovações obrigatórias             |
|----------------|-------------------------------------|
| `develop`      | Nay (Reviewer) + Rafa (Tech Lead) |
| `main`         | Rafa + aprovação humana             |

### CI/CD no PR

- Pipeline deve passar 100% antes do merge
- Erick executa SAST e secret scan automaticamente no PR
- Dani executa contrato e regressão no PR (ambientes efêmeros)

---

## Padrão de Commits

### Formato

```
<tipo>(<escopo>): <mensagem no imperativo, em português>
```

### Tipos

| Tipo       | Uso                                          |
|------------|----------------------------------------------|
| `feat`     | Nova funcionalidade                          |
| `fix`      | Correção de bug                              |
| `refactor` | Refatoração sem mudança de comportamento     |
| `test`     | Adição ou modificação de testes              |
| `docs`     | Documentação                                 |
| `infra`    | Infraestrutura, pipeline, configuração       |
| `security` | Correção de vulnerabilidade                  |
| `chore`    | Tarefas de manutenção sem impacto no produto |

### Exemplos

```
feat(pagamentos): adiciona endpoint de estorno com validação de prazo
fix(autenticacao): corrige expiração incorreta do refresh token
refactor(pedidos): extrai lógica de cálculo de frete para serviço dedicado
test(pagamentos): adiciona testes de contrato para o provedor de cartão
security(deps): atualiza library JWT para corrigir CVE-2026-XXXX
```

### Regras
- Mensagem no **imperativo** (adiciona, corrige, extrai — não "adicionado" ou "adicionando")
- Máximo **72 caracteres** no título
- Commits separados por tema (não agrupar mudanças não relacionadas)
- Gerado pela skill `Padronização de Commits` de Marcus
