"""
agents/marcus.py — Nó Marcus no grafo LangGraph.

Agente dev que usa tools para criar arquivos reais no workspace.
"""
from __future__ import annotations

import os

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse import observe, get_client

from swarm.prompts import MARCUS
from swarm.state import SwarmState
from swarm.tools import FILESYSTEM_TOOLS, GIT_TOOLS

langfuse = get_client()

ALL_TOOLS = FILESYSTEM_TOOLS + GIT_TOOLS
_llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022", temperature=0
).bind_tools(ALL_TOOLS)

# Mapa name → função para executar tools
TOOL_MAP = {t.name: t for t in ALL_TOOLS}


@observe(name="marcus", as_type="agent")
def marcus_node(state: SwarmState) -> dict:
    """Nó Marcus: implementa a demanda usando tools de filesystem e git."""
    routing = state.get("massuia_result", {})
    workspace = os.environ.get("SWARM_WORKSPACE", r"C:\Dev\workspace-ia-projects")

    print(f"\n[Marcus] Implementando: {state['summary']}")
    print(f"[Marcus] Workspace: {workspace}")

    langfuse.update_current_span(
        input={"summary": state["summary"], "workspace": workspace},
        metadata={"agent": "marcus", "demand_type": state["demand_type"]},
    )

    system_prompt = MARCUS + f"\n\n## Workspace\nTodos os arquivos devem ser criados em: {workspace}"
    user_prompt = f"""Demanda: {state['demand_text']}

Tipo: {state['demand_type']}
Resumo: {state['summary']}
Contexto técnico: {routing.get('context', 'Nenhum contexto adicional')}
Prioridade: {state['priority']}

Execute o fluxo completo:
1. Verifique os arquivos existentes com list_files
2. Inicialize o git se necessário com git_init
3. Crie uma branch com git_create_branch usando o padrão feat/<descricao>
4. Implemente o código com write_file
5. Escreva os testes
6. Faça o commit com git_commit

Ao final, confirme o que foi criado."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    files_created = []
    total_input_tokens = 0
    total_output_tokens = 0
    iterations = 0

    # Loop de tool-calling (ReAct)
    while iterations < 15:
        iterations += 1
        response = _llm.invoke(messages)

        total_input_tokens += response.usage_metadata.get("input_tokens", 0)
        total_output_tokens += response.usage_metadata.get("output_tokens", 0)
        messages.append(response)

        # Se não há tool calls, o agente terminou
        if not response.tool_calls:
            break

        # Executar cada tool call
        for tc in response.tool_calls:
            tool_fn = TOOL_MAP.get(tc["name"])
            if not tool_fn:
                result = f"❌ Tool desconhecida: {tc['name']}"
            else:
                try:
                    result = tool_fn.invoke(tc["args"])
                    if tc["name"] == "write_file":
                        files_created.append(tc["args"].get("relative_path", ""))
                    print(f"  [tool:{tc['name']}] {str(result)[:80]}")
                except Exception as e:
                    result = f"❌ Erro: {e}"

            from langchain_core.messages import ToolMessage
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

    langfuse.update_current_generation(
        model="claude-3-5-sonnet-20241022",
        usage_details={"input": total_input_tokens, "output": total_output_tokens},
    )

    final_message = response.content if hasattr(response, "content") else ""
    print(f"[Marcus] ✅ {len(files_created)} arquivo(s) criado(s): {files_created}")

    langfuse.update_current_span(
        output={"files_created": files_created, "iterations": iterations},
    )

    return {
        "marcus_result": {
            "files_created": files_created,
            "summary": final_message[:500],
            "iterations": iterations,
            "tokens": total_input_tokens + total_output_tokens,
        },
        "current_agent": "isa",
        "status": "reviewing",
        "messages": messages[2:],  # apenas mensagens novas
    }
