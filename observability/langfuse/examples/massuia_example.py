"""
Massuia — Exemplo de Supervisor com routing instrumentado.

Demonstra como o agente orquestrador usa DemandTracker para
rastrear o ciclo de vida completo de uma demanda e registrar
a decisão de routing para o agente correto.
"""

import os

from observability.langfuse.instrumentation import DemandTracker, trace_skill

# ---------------------------------------------------------------------------
# Configurar variáveis de ambiente antes de importar (ou use python-dotenv)
# ---------------------------------------------------------------------------
os.environ.setdefault("LANGFUSE_PUBLIC_KEY", "pk-lf-...")
os.environ.setdefault("LANGFUSE_SECRET_KEY", "sk-lf-...")
os.environ.setdefault("LANGFUSE_HOST", "http://localhost:3000")

# ---------------------------------------------------------------------------
# Mapa de routing: tipo de demanda → agente responsável
# Ref: SPEC-V2.md §8 Orquestração
# ---------------------------------------------------------------------------
ROUTING_MAP = {
    "feature":   "marcus",
    "bug":       "marcus",
    "hotfix":    "marcus",
    "refactor":  "marcus",
    "infra":     "eric",
    "security":  "erick",
    "db":        "alexandre",
    "review":    "nay",
    "docs":      "manu",
    "test":      "dani",
    "agile":     "isa",
}


# ---------------------------------------------------------------------------
# Skill de classificação de demanda
# ---------------------------------------------------------------------------
@trace_skill(agent_name="massuia", skill_name="classify_demand")
def classify_demand(trace, demand: dict) -> str:
    """
    Classifica o tipo da demanda.
    Em produção, esta função chamaria um LLM para classificar.
    """
    return demand.get("type", "unknown")


# ---------------------------------------------------------------------------
# Skill de routing
# ---------------------------------------------------------------------------
@trace_skill(agent_name="massuia", skill_name="route_demand")
def route_demand(trace, demand_type: str) -> str:
    """Retorna o agente responsável para o tipo de demanda."""
    return ROUTING_MAP.get(demand_type, "rafa")  # Rafa como fallback técnico


# ---------------------------------------------------------------------------
# Agente Massuia
# ---------------------------------------------------------------------------
class Massuia:
    """
    Supervisor do swarm — recebe demandas e roteia para o agente correto.
    Ref: SPEC-V2.md §5 — Massuia
    """

    def __init__(self) -> None:
        self.tracker = DemandTracker()

    def handle(self, demand: dict) -> dict:
        """
        Processa uma nova demanda:
        1. Inicia o trace unificado
        2. Classifica o tipo
        3. Determina o agente destino
        4. Registra o handoff
        5. Retorna routing decision
        """
        # Inicia o trace — este trace_id persiste por toda a demanda
        demand_id = self.tracker.start(demand)
        trace = self.tracker.get_trace(demand_id)

        # Classificar e rotear
        demand_type = classify_demand(trace, demand)
        target_agent = route_demand(trace, demand_type)

        # Registrar handoff
        self.tracker.handoff(
            demand_id=demand_id,
            from_agent="massuia",
            to_agent=target_agent,
            reason=f"Tipo '{demand_type}' mapeado para '{target_agent}'",
        )

        routing_decision = {
            "demand_id": demand_id,
            "demand_type": demand_type,
            "target_agent": target_agent,
            "status": "routed",
        }

        print(f"[Massuia] Demanda {demand_id} → {target_agent} ({demand_type})")
        return routing_decision


# ---------------------------------------------------------------------------
# Exemplo de uso
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    massuia = Massuia()

    # Simular recebimento de demandas
    demandas = [
        {
            "demand_id": "D-2026-001",
            "type": "feature",
            "description": "Adicionar autenticação OAuth2 no serviço de usuários",
            "requester": "product-team",
            "priority": "high",
        },
        {
            "demand_id": "D-2026-002",
            "type": "infra",
            "description": "Configurar pipeline de CD para o serviço de pagamentos",
            "requester": "dev-team",
            "priority": "normal",
        },
        {
            "demand_id": "D-2026-003",
            "type": "security",
            "description": "Revisar dependências com vulnerabilidades CVE-2026-XXXX",
            "requester": "security-team",
            "priority": "critical",
        },
    ]

    for demanda in demandas:
        resultado = massuia.handle(demanda)
        print(f"  → {resultado}\n")

    print("✅ Traces registrados no LangFuse: http://localhost:3000")
