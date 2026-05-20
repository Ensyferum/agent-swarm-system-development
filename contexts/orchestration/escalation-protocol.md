# Protocolo de Escalação

> Mantido por: **Rafa (Líder Técnico)**
> Define **quando** e **como** um agente deve escalar um problema para outro agente ou para validação humana.

---

## Níveis de Escalação

### Nível 1 — Auto-resolução (Agente)
- **Gatilho:** problema identificado na primeira iteração
- **Ação:** agente tenta resolver autonomamente
- **Limite:** até **2 iterações** sem progresso
- **Documentação:** registrar tentativas no relatório de execução

### Nível 2 — Escalação para Rafa (Líder Técnico)
- **Gatilho:** após 2 iterações sem resolução OU ambiguidade de decisão técnica
- **Casos típicos:**
  - Conflito entre padrões definidos e requisito recebido
  - Dúvida sobre qual serviço deve ser responsável por uma lógica
  - Decisão com impacto arquitetural (novo serviço, nova dependência)
  - Conflito entre dois agentes sobre abordagem técnica
- **Ação:** agente para a execução, emite relatório de bloqueio para Rafa, aguarda diretiva
- **SLA esperado de Rafa:** resposta na mesma sessão

### Nível 3 — Escalação para Manu (Product Owner)
- **Gatilho:** ambiguidade em regra de negócio ou critério de aceite
- **Casos típicos:**
  - Requisito contraditório entre histórias diferentes
  - Comportamento esperado não está claro na história
  - Critério de aceite insuficiente para implementação
- **Ação:** Rafa ou o agente bloqueado emite relatório para Manu com a dúvida estruturada (contexto + opções + impacto)
- **Manu documenta a decisão** como critério de aceite atualizado na história

### Nível 4 — Pausa para Validação Humana
- **Gatilho:** qualquer das condições abaixo
  - Decisão arquitetural **irreversível** ou de alto custo para desfazer
  - Loop de falhas: >3 iterações sem progresso em qualquer nível
  - Conflito não resolvido entre agentes após escalação para Rafa
  - Issue de segurança crítica identificada por Erick
  - Resultado de DAST com impacto crítico em produção
- **Ação:** **todo o swarm pausa**; relatório consolidado emitido por Rafa para o humano responsável
- **Retomada:** somente após aprovação humana explícita

---

## Matriz de Escalação por Agente

| Agente   | Escala para quem (técnico) | Escala para quem (negócio) |
|----------|----------------------------|----------------------------|
| Marcus   | Rafa                       | —                          |
| Dani     | Rafa                       | Manu (critério de aceite)  |
| Nay    | Rafa                       | —                          |
| Eric      | Rafa                       | —                          |
| Erick     | Rafa → Humano (se crítico) | —                          |
| Alexandre      | Rafa                       | Manu (regra de dados)      |
| Rafa     | Humano                     | Manu                       |
| Manu     | Humano                     | Humano                     |

---

## Formato do Relatório de Bloqueio

Todo agente ao escalar deve emitir relatório com:

```
BLOQUEIO — <Nome do Agente> (<Codinome>)
Task: <descrição da task em execução>
Nível de escalação: <1 | 2 | 3 | 4>
Motivo: <descrição clara do bloqueio>
Iterações realizadas: <N>
Tentativas anteriores: <resumo do que foi tentado>
Opções consideradas:
  A) <opção A> — impacto: <...>
  B) <opção B> — impacto: <...>
Aguardando decisão de: <agente ou humano>
```
