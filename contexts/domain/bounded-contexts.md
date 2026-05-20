# Bounded Contexts

> Documento mantido por: **Rafa (Líder Técnico)** + **Manu (Product Owner)**
> Define as fronteiras de cada domínio e como eles se comunicam.

---

## O que é um Bounded Context?

É o limite dentro do qual um modelo de domínio específico é válido e consistente. Dois contextos podem usar o mesmo termo com significados diferentes — este documento mapeia essas diferenças e define as traduções (Anti-Corruption Layer quando necessário).

---

## Contextos Definidos

| Contexto | Responsável de Negócio | Serviços Associados | Banco de Dados |
|----------|------------------------|---------------------|----------------|
| —        | —                      | —                   | —              |

---

## Mapa de Relacionamentos

```
[ Contexto A ] ──── (evento: NomeDo Evento) ──── [ Contexto B ]
```

*(Atualizar conforme novos domínios forem identificados)*

---

## Regras de Integração entre Contextos

- Comunicação entre contextos **sempre** via API REST ou mensageria assíncrona.
- **Nunca** acesso direto ao banco de outro contexto.
- Dados compartilhados devem ter um **Shared Kernel** explicitamente documentado aqui.
- Dados que precisam ser traduzidos entre contextos usam **Anti-Corruption Layer (ACL)**.

---

## Anti-Corruption Layers Definidas

| De (Contexto) | Para (Contexto) | Tipo de Tradução | Responsável |
|---------------|-----------------|------------------|-------------|
| —             | —               | —                | —           |
