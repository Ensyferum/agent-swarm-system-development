"""
agents/massuia.py — Nó Massuia no grafo LangGraph.

Recebe a demanda, classifica o tipo e decide o agente destino.
"""
from __future__ import annotations

import json
import os

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse import observe, get_client

from swarm.prompts import MASSUIA
from swarm.state import SwarmState

langfuse = get_client()
_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)


@observe(name="massuia", as_type="agent")
def massuia_node(state: SwarmState) -> dict:
    """Nó Massuia: classifica e roteia a demanda."""
    print(f"\n[Massuia] Analisando demanda: {state['demand_text'][:80]}...")

    langfuse.update_current_span(
        input={"demand_text": state["demand_text"]},
        metadata={"agent": "massuia"},
    )

    messages = [
        SystemMessage(content=MASSUIA),
        HumanMessage(content=f"Demanda recebida:\n\n{state['demand_text']}"),
    ]

    response = _llm.invoke(messages)

    langfuse.update_current_generation(
        model="claude-3-5-sonnet-20241022",
        usage_details={
            "input": response.usage_metadata.get("input_tokens", 0),
            "output": response.usage_metadata.get("output_tokens", 0),
        },
        input=state["demand_text"],
        output=response.content,
    )

    try:
        routing = json.loads(response.content.strip())
    except json.JSONDecodeError:
        # Extrair JSON de resposta com texto ao redor
        import re
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        routing = json.loads(match.group()) if match else {}

    print(f"[Massuia] → {routing.get('target_agent', '?')} ({routing.get('demand_type', '?')})")

    langfuse.update_current_span(output=routing)

    return {
        "demand_type": routing.get("demand_type", "unknown"),
        "target_agent": routing.get("target_agent", "marcus"),
        "priority": routing.get("priority", "normal"),
        "summary": routing.get("summary", ""),
        "massuia_result": routing,
        "current_agent": routing.get("target_agent", "marcus"),
        "status": "executing",
        "messages": [response],
    }
