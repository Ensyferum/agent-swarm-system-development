# Políticas de Segurança

> Mantido por: **Erick (SecOps)**
> De cumprimento obrigatório por todos os agentes. Violações bloqueiam o fluxo de deploy.

---

## 1. Gestão de Secrets e Credenciais

- ❌ **Proibido:** secrets, tokens, passwords, API keys em código fonte ou arquivos commitados
- ✅ **Obrigatório:** uso de gerenciador de segredos (Vault, AWS Secret Manager, etc.)
- ✅ **Obrigatório:** `.env` no `.gitignore`; `.env.example` com valores fictícios no repositório
- Rotação de secrets críticos: mínimo a cada **90 dias**

## 2. Autenticação e Autorização

- Todo endpoint exposto externamente **deve** ser autenticado (JWT, OAuth2)
- Princípio do menor privilégio: serviços acessam apenas os recursos que precisam
- Tokens JWT: expiração máxima de **1 hora** para access tokens
- Nenhum dado sensível em tokens JWT (senha, número de cartão, etc.)

## 3. Comunicação

- HTTPS obrigatório em todos os ambientes (homolog e produção)
- Comunicação interna entre serviços via mTLS ou rede privada isolada
- Nenhum serviço expõe porta de banco de dados externamente

## 4. Dependências

- Scan de CVEs obrigatório antes de todo merge (skill `dependency vulnerability check` de Erick)
- Dependências com CVE crítico ou alto **bloqueiam** o merge
- Dependências devem ser fixadas em versões específicas (sem `latest` em produção)
- Atualização de dependências com CVEs: máximo **48h** para críticos

## 5. Código

- SAST obrigatório antes de todo merge (skill `SAST scan` de Erick)
- Issues críticos e altos de SAST **bloqueiam** o merge
- Sem queries SQL construídas por concatenação de string (SQL Injection)
- Sem deserialização de dados não confiáveis sem validação
- Validação e sanitização de toda entrada externa

## 6. Infraestrutura

- Imagens Docker: base apenas em imagens oficiais e verificadas
- Containers não rodam como root
- Recursos de infraestrutura com o menor conjunto de permissões necessário
- Secrets de infraestrutura gerenciados por Eric (DevOps) via IaC

## 7. Auditoria e Monitoramento

- Todo acesso a dados sensíveis deve gerar log de auditoria
- Logs **não devem** conter dados sensíveis (PII, senhas, tokens)
- Alertas de segurança configurados para: tentativas de autenticação falhas (>5), acesso a dados em volume anormal

## 8. Classificação de Issues de Segurança

| Severidade | Definição                                    | Ação obrigatória             |
|------------|----------------------------------------------|------------------------------|
| Crítico    | Execução remota, vazamento de dados massivo  | Bloquear, corrigir imediatamente |
| Alto       | Elevação de privilégio, bypass de autenticação | Bloquear merge                |
| Médio      | Exposição de dados não críticos              | Corrigir no próximo ciclo     |
| Baixo      | Boas práticas, hardening                     | Registrar em tech-debt        |

---

## Checklist de Segurança por Ciclo de Entrega

- [ ] SAST executado sem bloqueios
- [ ] Scan de dependências sem CVEs críticos/altos
- [ ] Secret scanning sem resultados positivos
- [ ] DAST executado em homolog (Erick executa após deploy de Eric)
- [ ] Relatório de segurança emitido por Erick
