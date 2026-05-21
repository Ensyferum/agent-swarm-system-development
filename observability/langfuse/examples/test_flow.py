"""
Teste de fluxo completo: Massuia → Marcus → Isa
Compatível com LangFuse SDK v4 (OpenTelemetry-based)
"""

import os
import sys
import time

# Carregar variáveis do .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    for line in open(env_path):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

# LangFuse v4 usa LANGFUSE_HOST (o SDK da UI chama de BASE_URL)
if not os.environ.get("LANGFUSE_HOST"):
    os.environ["LANGFUSE_HOST"] = os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000")

from langfuse import observe, get_client

langfuse = get_client()

print("=" * 60)
print("  TESTE DE FLUXO — Agent Swarm + LangFuse v4")
print("=" * 60)

if not langfuse.auth_check():
    print("❌ Falha de autenticação. Verifique as chaves no .env")
    sys.exit(1)
print("✅ Conectado ao LangFuse:", os.environ["LANGFUSE_HOST"])

# ------------------------------------------------------------------
# Demanda de teste
# ------------------------------------------------------------------
DEMAND = {
    "demand_id": "D-TEST-001",
    "type": "feature",
    "description": "Implementar tela de login com autenticação OAuth2",
    "requester": "product-team",
    "priority": "high",
}

print(f"\n📥 Demanda: {DEMAND['demand_id']} — {DEMAND['description']}\n")

# ------------------------------------------------------------------
# Skills como funções decoradas com @observe
# ------------------------------------------------------------------

@observe(name="massuia.classify_demand", as_type="span")
def classify_demand(demand: dict) -> str:
    time.sleep(0.1)
    langfuse.update_current_generation(
        model="gpt-4o-mini",
        usage_details={"input": 120, "output": 15},
        input=f"Classifique: {demand['description']}",
        output="feature",
    )
    return demand.get("type", "unknown")


@observe(name="massuia.route_demand", as_type="span")
def route_demand(demand_type: str) -> str:
    routing = {
        "feature": "marcus", "bug": "marcus", "hotfix": "marcus",
        "infra": "eric", "security": "erick", "db": "alexandre",
    }
    return routing.get(demand_type, "rafa")


@observe(name="marcus.analyze_requirement", as_type="span")
def analyze_requirement(demand: dict) -> dict:
    time.sleep(0.2)
    langfuse.update_current_generation(
        model="gpt-4o",
        usage_details={"input": 480, "output": 210},
        input=demand["description"],
        output="Tasks: [criar schema OAuth, implementar handler, adicionar testes]",
    )
    return {"tasks": ["criar schema OAuth", "implementar handler", "adicionar testes"]}


@observe(name="marcus.implement_feature", as_type="span")
def implement_feature(tasks: list) -> dict:
    time.sleep(0.3)
    langfuse.update_current_generation(
        model="gpt-4o",
        usage_details={"input": 1100, "output": 750},
    )
    return {
        "files": ["src/auth/oauth2.py", "src/auth/tests/test_oauth2.py", "src/main.py"],
        "pr_ready": True,
    }


@observe(name="marcus.create_pr_description", as_type="span")
def create_pr_description(demand: dict) -> str:
    time.sleep(0.1)
    langfuse.update_current_generation(
        model="gpt-4o-mini",
        usage_details={"input": 280, "output": 120},
    )
    return f"## {demand['description']}\n\nImplementação de OAuth2 completa."


@observe(name="isa.update_task_status", as_type="span")
def update_task_status(task_id: str, status: str, agent: str) -> dict:
    return {"task_id": task_id, "status": status, "updated_by": agent}


@observe(name="isa.generate_sprint_report", as_type="span")
def generate_sprint_report(tasks: list) -> dict:
    done = [t for t in tasks if t["status"] == "done"]
    rate = round(len(done) / len(tasks) * 100, 1)
    return {"done": len(done), "total": len(tasks), "completion_pct": rate}


# ------------------------------------------------------------------
# Fluxo principal: cada agente é um @observe que agrupa suas skills
# ------------------------------------------------------------------

@observe(name="massuia", as_type="agent")
def run_massuia(demand: dict) -> dict:
    demand_type = classify_demand(demand)
    target = route_demand(demand_type)
    langfuse.update_current_span(
        metadata={"agent": "massuia", "demand_id": demand["demand_id"],
                  "demand_type": demand_type, "routed_to": target},
    )
    print(f"[Massuia] ✅ '{demand_type}' → {target}")
    return {"demand_type": demand_type, "target_agent": target}


@observe(name="marcus", as_type="agent")
def run_marcus(demand: dict) -> dict:
    analysis = analyze_requirement(demand)
    impl = implement_feature(analysis["tasks"])
    pr = create_pr_description(demand)
    langfuse.update_current_span(
        metadata={"agent": "marcus", "demand_id": demand["demand_id"],
                  "files_created": len(impl["files"])},
    )
    print(f"[Marcus]  ✅ {len(impl['files'])} arquivos gerados, PR pronto")
    return {"files": impl["files"], "pr_description": pr}


@observe(name="isa", as_type="agent")
def run_isa(demand: dict, marcus_result: dict) -> dict:
    update_task_status(demand["demand_id"], "done", "marcus")
    sprint_tasks = [
        {"task_id": "T-101", "status": "done"},
        {"task_id": "T-102", "status": "done"},
        {"task_id": demand["demand_id"], "status": "done"},
        {"task_id": "T-104", "status": "in_progress"},
    ]
    report = generate_sprint_report(sprint_tasks)
    langfuse.update_current_span(
        metadata={"agent": "isa", "demand_id": demand["demand_id"],
                  "completion_pct": report["completion_pct"]},
    )
    print(f"[Isa]     ✅ Sprint: {report['done']}/{report['total']} ({report['completion_pct']}%)")
    return report


@observe(name=f"demand.{DEMAND['demand_id']}", as_type="span")
def run_full_flow(demand: dict) -> dict:
    """Trace raiz — agrupa todo o fluxo da demanda."""
    langfuse.update_current_span(
        input={"demand_id": demand["demand_id"], "description": demand["description"]},
        metadata={"demand_id": demand["demand_id"], "type": demand["type"],
                  "priority": demand["priority"]},
    )

    routing = run_massuia(demand)
    marcus_result = run_marcus(demand)
    isa_result = run_isa(demand, marcus_result)

    # Capturar trace_id enquanto ainda estamos dentro do contexto
    trace_id = langfuse.get_current_trace_id()

    langfuse.update_current_span(
        output={"status": "success", "files": marcus_result["files"],
                "completion_pct": isa_result["completion_pct"]},
    )
    return {"routing": routing, "marcus": marcus_result, "isa": isa_result,
            "_trace_id": trace_id}


# ------------------------------------------------------------------
# Executar
# ------------------------------------------------------------------
result = run_full_flow(DEMAND)
trace_id = result.get("_trace_id", "N/A")
langfuse.flush()

print("\n" + "=" * 60)
print("  FLUXO CONCLUÍDO")
print("=" * 60)
print(f"  Trace ID : {trace_id}")
print(f"  Arquivos : {result['marcus']['files']}")
print(f"  Sprint   : {result['isa']['completion_pct']}% concluído")
print()
print(f"🔍 Ver trace: {os.environ['LANGFUSE_HOST']}/trace/{trace_id}")
print("=" * 60)

