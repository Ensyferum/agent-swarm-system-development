"""
agents/isa.py — Nó Isa no grafo LangGraph.

Registra o resultado da execução e gera métricas da sprint.
"""
from __future__ import annotations

import json
import re

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse import observe, get_client

from swarm.prompts import ISA
from swarm.state import SwarmState

langfuse = get_client()
_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)


@observe(name="isa", as_type="agent")
def isa_node(state: SwarmState) -> dict:
    """Nó Isa: registra o resultado e gera relatório de sprint."""
    marcus_result = state.get("marcus_result", {})

    print(f"\n[Isa] Registrando resultado da demanda {state['demand_id']}...")

    langfuse.update_current_span(
        input={"marcus_result": marcus_result},
        metadata={"agent": "isa"},
    )

    user_prompt = f"""Demanda concluída:
- ID: {state['demand_id']}
- Tipo: {state['demand_type']}
- Executado por: marcus
- Resumo: {state['summary']}
- Arquivos criados: {marcus_result.get('files_created', [])}
- Resultado: {marcus_result.get('summary', '')[:300]}

Registre o status e gere as métricas."""

    messages = [
        SystemMessage(content=ISA),
        HumanMessage(content=user_prompt),
    ]

    response = _llm.invoke(messages)

    langfuse.update_current_generation(
        model="claude-3-5-sonnet-20241022",
        usage_details={
            "input": response.usage_metadata.get("input_tokens", 0),
            "output": response.usage_metadata.get("output_tokens", 0),
        },
    )

    try:
        report = json.loads(response.content.strip())
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        report = json.loads(match.group()) if match else {"status": "done"}

    print(f"[Isa] ✅ Status: {report.get('status')} | {report.get('summary', '')[:60]}")

    langfuse.update_current_span(output=report)

    return {
        "isa_result": report,
        "status": "done",
        "current_agent": "done",
        "messages": [response],
    }
