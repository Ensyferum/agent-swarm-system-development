"""
Isa — Exemplo de Agente Ágil com métricas de task board.

Demonstra como a Isa usa LangFuse para rastrear mudanças de status
de tarefas, ciclo de tempo e geração de relatórios de andamento do projeto.
"""

import os
from datetime import datetime, timezone

os.environ.setdefault("LANGFUSE_PUBLIC_KEY", "pk-lf-...")
os.environ.setdefault("LANGFUSE_SECRET_KEY", "sk-lf-...")
os.environ.setdefault("LANGFUSE_HOST", "http://localhost:3000")

from langfuse import Langfuse
from observability.langfuse.instrumentation import BaseAgent, trace_skill


# ---------------------------------------------------------------------------
# Skills da Isa
# ---------------------------------------------------------------------------

@trace_skill(agent_name="isa", skill_name="update_task_status")
def update_task_status(trace, task_id: str, new_status: str, agent: str) -> dict:
    """
    Atualiza o status de uma tarefa no task board.
    Ref: contexts/quality/task-board/README.md
    """
    valid_statuses = {"backlog", "in_progress", "review", "blocked", "done"}
    if new_status not in valid_statuses:
        raise ValueError(f"Status inválido: '{new_status}'. Válidos: {valid_statuses}")

    return {
        "task_id": task_id,
        "new_status": new_status,
        "updated_by": agent,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@trace_skill(agent_name="isa", skill_name="calculate_cycle_time")
def calculate_cycle_time(trace, started_at: str, completed_at: str) -> dict:
    """Calcula o cycle time de uma tarefa em horas."""
    start = datetime.fromisoformat(started_at)
    end = datetime.fromisoformat(completed_at)
    delta = end - start
    hours = round(delta.total_seconds() / 3600, 2)
    return {"cycle_time_hours": hours, "within_sla": hours <= 48}


@trace_skill(agent_name="isa", skill_name="generate_sprint_report")
def generate_sprint_report(trace, sprint_id: str, tasks: list) -> dict:
    """
    Gera um relatório de andamento da sprint.
    Ref: SPEC-V2.md §5 — Isa skills: generate-sprint-report
    """
    done = [t for t in tasks if t.get("status") == "done"]
    blocked = [t for t in tasks if t.get("status") == "blocked"]
    in_progress = [t for t in tasks if t.get("status") == "in_progress"]

    completion_rate = round(len(done) / len(tasks) * 100, 1) if tasks else 0

    cycle_times = [t.get("cycle_time_hours", 0) for t in done if t.get("cycle_time_hours")]
    avg_cycle_time = round(sum(cycle_times) / len(cycle_times), 2) if cycle_times else 0

    return {
        "sprint_id": sprint_id,
        "total_tasks": len(tasks),
        "done": len(done),
        "blocked": len(blocked),
        "in_progress": len(in_progress),
        "completion_rate_pct": completion_rate,
        "avg_cycle_time_hours": avg_cycle_time,
        "impediments": [t.get("impediment") for t in blocked if t.get("impediment")],
    }


@trace_skill(agent_name="isa", skill_name="detect_impediments")
def detect_impediments(trace, tasks: list) -> list:
    """
    Detecta tarefas bloqueadas há mais de 24h e gera alertas.
    """
    impediments = []
    now = datetime.now(timezone.utc)

    for task in tasks:
        if task.get("status") != "blocked":
            continue
        blocked_since_str = task.get("blocked_since")
        if not blocked_since_str:
            continue
        blocked_since = datetime.fromisoformat(blocked_since_str)
        hours_blocked = (now - blocked_since).total_seconds() / 3600
        if hours_blocked > 24:
            impediments.append({
                "task_id": task["task_id"],
                "hours_blocked": round(hours_blocked, 1),
                "impediment": task.get("impediment", "Não especificado"),
                "action": "escalate_to_massuia",
            })

    return impediments


# ---------------------------------------------------------------------------
# Agente Isa
# ---------------------------------------------------------------------------

class Isa(BaseAgent):
    """
    Agente de controle ágil — monitora tarefas e gera métricas de projeto.
    Ref: SPEC-V2.md §5 — Isa
    """

    def __init__(self) -> None:
        super().__init__(name="isa")

    def execute(self, demand: dict, trace) -> dict:
        """
        Fluxo de atualização e monitoramento:
        1. Atualizar status da tarefa
        2. Calcular cycle time (se concluída)
        3. Detectar impedimentos
        4. Gerar relatório da sprint
        """
        demand_id = demand["demand_id"]
        action = demand.get("action", "status_update")

        print(f"[Isa] Processando ação '{action}' para {demand_id}")

        # Atualizar status
        task_update = update_task_status(
            trace,
            task_id=demand.get("task_id", demand_id),
            new_status=demand.get("new_status", "in_progress"),
            agent=demand.get("triggering_agent", "unknown"),
        )

        # Calcular cycle time se a tarefa foi concluída
        cycle_info = {}
        if demand.get("new_status") == "done" and demand.get("started_at") and demand.get("completed_at"):
            cycle_info = calculate_cycle_time(
                trace,
                started_at=demand["started_at"],
                completed_at=demand["completed_at"],
            )

        # Detectar impedimentos na sprint atual
        current_tasks = demand.get("sprint_tasks", [])
        impediments = detect_impediments(trace, current_tasks)

        # Gerar relatório da sprint
        sprint_report = generate_sprint_report(
            trace,
            sprint_id=demand.get("sprint_id", "sprint-unknown"),
            tasks=current_tasks,
        )

        # Registrar evento de alerta se houver impedimentos críticos
        if impediments:
            self.log_event(trace, "impediments.detected", {
                "count": len(impediments),
                "tasks": [i["task_id"] for i in impediments],
            })
            print(f"[Isa] ⚠️  {len(impediments)} impedimentos detectados — escalar para Massuia")

        return {
            "task_update": task_update,
            "cycle_time": cycle_info,
            "sprint_report": sprint_report,
            "impediments_detected": len(impediments),
            "impediments": impediments,
        }


# ---------------------------------------------------------------------------
# Exemplo de uso
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    isa = Isa()

    sprint_tasks = [
        {"task_id": "T-101", "status": "done", "cycle_time_hours": 12.5},
        {"task_id": "T-102", "status": "done", "cycle_time_hours": 8.0},
        {"task_id": "T-103", "status": "in_progress"},
        {
            "task_id": "T-104",
            "status": "blocked",
            "impediment": "Aguardando aprovação de acesso ao banco",
            "blocked_since": "2026-05-19T10:00:00+00:00",
        },
        {"task_id": "T-105", "status": "backlog"},
    ]

    demand = {
        "demand_id": "D-2026-001",
        "action": "status_update",
        "task_id": "T-103",
        "new_status": "done",
        "triggering_agent": "marcus",
        "started_at": "2026-05-20T08:00:00+00:00",
        "completed_at": "2026-05-20T16:00:00+00:00",
        "sprint_id": "sprint-42",
        "sprint_tasks": sprint_tasks,
    }

    resultado = isa.run(demand)
    print(f"\n📊 Sprint Report: {resultado['sprint_report']}")
    print(f"⏱️  Cycle Time: {resultado['cycle_time']}")
    print(f"🔍 Trace: http://localhost:3000/trace/{resultado['_trace_id']}")
