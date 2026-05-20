# Repositório de Testes Reutilizáveis

> Mantido por: **Dani (QA)**
> Centraliza todos os recursos de teste que podem ser reaproveitados entre features e domínios.

---

## Estrutura

```
test-repository/
├── bdd/
│   └── <dominio>/
│       └── <feature>.feature       # Cenários BDD reutilizáveis
├── e2e/
│   └── <dominio>/
│       └── <feature>/              # Keywords e recursos Robot Framework
├── contract/
│   └── <servico>/
│       └── <consumidor>-<provedor>.json  # Contratos Pact
├── performance/
│   └── <dominio>/
│       └── <cenario>.js            # Scripts k6 / Locust
└── data/
    └── <dominio>/
        └── fixtures.json           # Massa de dados reutilizável
```

---

## Convenções

### BDD (`.feature`)
- Escrito em português
- Um arquivo por funcionalidade
- Gerado via skill `Transformação de BDD em cenário de Teste` de Dani
- Nomenclatura: `<verbo-no-infinitivo>-<objeto>.feature` (ex: `realizar-pagamento.feature`)

### E2E (Robot Framework)
- Um diretório por domínio
- Keywords reutilizáveis em `<dominio>/keywords/`
- Suíte por funcionalidade
- Gerado via skill `Scaffolding para geração de projetos do dominio` de Dani

### Contract Testing (Pact)
- Um arquivo por par consumidor-provedor
- Executado via skill `contract-testing` de Dani
- Deve ser validado no CI antes do deploy do provedor

### Performance (k6/Locust)
- Um script por cenário de carga
- Thresholds documentados no próprio script
- Gerado via skill `performance-testing` de Dani

---

## Índice de Testes por Domínio

| Domínio | BDD | E2E | Contract | Performance |
|---------|-----|-----|----------|-------------|
| —       | —   | —   | —        | —           |
