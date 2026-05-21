"""
State — define o estado compartilhado que flui pelo grafo LangGraph.
"""
from __future__ import annotations
from typing import Annotated, Any
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class SwarmState(TypedDict):
    # Mensagens trocadas no grafo (acumuladas)
    messages: Annotated[list, add_messages]

    # Dados da demanda
    demand_id: str
    demand_text: str
    demand_type: str
    target_agent: str
    priority: str
    summary: str

    # Resultados por agente
    massuia_result: dict[str, Any]
    marcus_result: dict[str, Any]
    isa_result: dict[str, Any]

    # Controle de fluxo
    current_agent: str
    status: str  # "routing" | "executing" | "reviewing" | "done" | "failed"
    error: str
