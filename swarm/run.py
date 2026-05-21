"""
run.py — Entrypoint do Agent Swarm.

Uso:
    # Variáveis necessárias no .env ou ambiente:
    # ANTHROPIC_API_KEY=sk-ant-...
    # LANGFUSE_PUBLIC_KEY=pk-lf-...
    # LANGFUSE_SECRET_KEY=sk-lf-...
    # LANGFUSE_HOST=http://localhost:3000
    # SWARM_WORKSPACE=C:\\Dev\\workspace-ia-projects

    python swarm/run.py "Crie uma API REST em Python com FastAPI para gerenciar tarefas"

    # Ou com mais detalhes:
    python swarm/run.py --id D-001 --priority high "Crie um módulo de autenticação JWT"
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path

# Carregar .env do projeto
_env_file = Path(__file__).parent.parent / "observability" / "langfuse" / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

# LANGFUSE_HOST alias
if not os.environ.get("LANGFUSE_HOST"):
    os.environ["LANGFUSE_HOST"] = os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000")

# Workspace padrão
os.environ.setdefault("SWARM_WORKSPACE", r"C:\Dev\workspace-ia-projects")

from langfuse import get_client, observe
from swarm.graph import swarm_graph

langfuse = get_client()


@observe(name="swarm.run", as_type="span")
def run_swarm(demand_text: str, demand_id: str = "", priority: str = "normal") -> dict:
    """Executa o fluxo completo do swarm para uma demanda."""
    if not demand_id:
        demand_id = f"D-{uuid.uuid4().hex[:8].upper()}"

    langfuse.update_current_span(
        input={"demand_id": demand_id, "demand_text": demand_text},
        metadata={"demand_id": demand_id, "priority": priority},
    )

    initial_state = {
        "messages": [],
        "demand_id": demand_id,
        "demand_text": demand_text,
        "demand_type": "",
        "target_agent": "",
        "priority": priority,
        "summary": "",
        "massuia_result": {},
        "marcus_result": {},
        "isa_result": {},
        "current_agent": "massuia",
        "status": "routing",
        "error": "",
    }

    print(f"\n{'='*60}")
    print(f"  AGENT SWARM — {demand_id}")
    print(f"  Workspace: {os.environ['SWARM_WORKSPACE']}")
    print(f"{'='*60}")
    print(f"  Demanda: {demand_text}")
    print(f"{'='*60}\n")

    result = swarm_graph.invoke(initial_state)

    trace_id = langfuse.get_current_trace_id()
    langfuse.update_current_span(output={"status": result.get("status"), "demand_id": demand_id})

    return {**result, "_trace_id": trace_id}


def main():
    parser = argparse.ArgumentParser(description="Agent Swarm — LangGraph + Anthropic + LangFuse")
    parser.add_argument("demand", nargs="+", help="Descrição da demanda")
    parser.add_argument("--id", dest="demand_id", default="", help="ID da demanda (opcional)")
    parser.add_argument("--priority", default="normal",
                        choices=["low", "normal", "high", "critical"])
    args = parser.parse_args()

    demand_text = " ".join(args.demand)

    # Validar API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY não configurada.")
        print("   Adicione ao arquivo observability/langfuse/.env:")
        print("   ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    result = run_swarm(demand_text, args.demand_id, args.priority)
    langfuse.flush()

    print(f"\n{'='*60}")
    print("  SWARM CONCLUÍDO")
    print(f"{'='*60}")
    print(f"  Status   : {result.get('status', '?')}")
    print(f"  Agente   : {result.get('target_agent', '?')}")
    print(f"  Arquivos : {result.get('marcus_result', {}).get('files_created', [])}")
    print(f"  Trace ID : {result.get('_trace_id', 'N/A')}")
    print(f"\n🔍 LangFuse: {os.environ['LANGFUSE_HOST']}/trace/{result.get('_trace_id', '')}")
    print(f"📁 Workspace: {os.environ['SWARM_WORKSPACE']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
