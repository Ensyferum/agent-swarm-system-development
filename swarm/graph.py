"""
graph.py — Grafo LangGraph do Agent Swarm.

Define os nós (agentes) e as arestas (roteamento condicional).

Fluxo:
  START → massuia → [router] → marcus → isa → END
                             ↘ (outros agentes futuros)
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from swarm.agents import isa_node, marcus_node, massuia_node
from swarm.state import SwarmState

# Agentes que Marcus pode substituir (expansão futura)
DEV_AGENTS = {"marcus", "feature", "bug", "hotfix", "refactor"}


def route_after_massuia(state: SwarmState) -> str:
    """
    Roteamento condicional após Massuia decidir o agente.
    Atualmente só Marcus está implementado — outros agentes
    podem ser adicionados aqui conforme o swarm cresce.
    """
    target = state.get("target_agent", "marcus")
    if target in DEV_AGENTS or target == "marcus":
        return "marcus"
    # Fallback: marcus lida com demandas não mapeadas
    return "marcus"


def build_graph() -> StateGraph:
    graph = StateGraph(SwarmState)

    # Nós
    graph.add_node("massuia", massuia_node)
    graph.add_node("marcus", marcus_node)
    graph.add_node("isa", isa_node)

    # Arestas
    graph.add_edge(START, "massuia")
    graph.add_conditional_edges("massuia", route_after_massuia, {"marcus": "marcus"})
    graph.add_edge("marcus", "isa")
    graph.add_edge("isa", END)

    return graph.compile()


# Instância compilada (reutilizável)
swarm_graph = build_graph()
