"""
demand_tracker — Rastreamento do ciclo de vida completo de uma demanda.

Responsável por registrar os eventos de transição entre agentes,
mantendo o trace unificado para toda a jornada de uma demanda no swarm.

Uso:
    from observability.langfuse.instrumentation.demand_tracker import DemandTracker

    tracker = DemandTracker()
    tracker.start(demand)
    tracker.handoff(demand_id, from_agent="massuia", to_agent="marcus")
    tracker.complete(demand_id, final_agent="marcus")
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from langfuse import Langfuse


class DemandTracker:
    """
    Rastreia o ciclo de vida de uma demanda através dos agentes do swarm.

    Mantém um mapa interno demand_id → trace para permitir que qualquer
    agente adicione eventos ao trace correto sem precisar passá-lo
    explicitamente.
    """

    def __init__(self) -> None:
        self._langfuse = Langfuse(
            public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
            secret_key=os.environ["LANGFUSE_SECRET_KEY"],
            host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000"),
        )
        self._active_traces: dict[str, Any] = {}

    def start(self, demand: dict[str, Any]) -> str:
        """
        Inicia o rastreamento de uma nova demanda.

        Args:
            demand: Deve conter: demand_id, type, description, requester

        Returns:
            O demand_id registrado.
        """
        demand_id = demand["demand_id"]
        demand_type = demand.get("type", "unknown")

        trace = self._langfuse.trace(
            id=demand_id,
            name=f"demand.{demand_type}",
            user_id=demand.get("requester"),
            session_id=demand_id,
            input={"description": demand.get("description", "")},
            metadata={
                "demand_type": demand_type,
                "priority": demand.get("priority", "normal"),
                "source": demand.get("source", "swarm"),
                "started_at": datetime.now(timezone.utc).isoformat(),
            },
            tags=[demand_type, "demand"],
        )

        self._active_traces[demand_id] = trace

        trace.event(
            name="demand.received",
            metadata={
                "agent": "massuia",
                "demand_id": demand_id,
                "type": demand_type,
            },
        )

        return demand_id

    def handoff(
        self,
        demand_id: str,
        from_agent: str,
        to_agent: str,
        reason: str = "",
    ) -> None:
        """
        Registra a transferência de uma demanda entre agentes.

        Args:
            demand_id:  ID da demanda sendo transferida.
            from_agent: Agente que está passando a demanda.
            to_agent:   Agente que irá receber a demanda.
            reason:     Motivo da transferência (opcional).
        """
        trace = self._get_trace(demand_id)
        trace.event(
            name="demand.handoff",
            metadata={
                "from_agent": from_agent,
                "to_agent": to_agent,
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    def escalate(
        self,
        demand_id: str,
        from_agent: str,
        to_agent: str,
        level: int,
        description: str,
    ) -> None:
        """
        Registra uma escalação conforme o escalation-protocol.md.

        Args:
            demand_id:   ID da demanda.
            from_agent:  Agente que escalou.
            to_agent:    Agente/humano que recebeu a escalação.
            level:       Nível 1-4 conforme escalation-protocol.md.
            description: Descrição do motivo da escalação.
        """
        trace = self._get_trace(demand_id)
        trace.event(
            name="escalation.triggered",
            metadata={
                "from_agent": from_agent,
                "to_agent": to_agent,
                "level": level,
                "description": description,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    def complete(
        self,
        demand_id: str,
        final_agent: str,
        status: str = "success",
        summary: str = "",
    ) -> None:
        """
        Marca uma demanda como concluída.

        Args:
            demand_id:   ID da demanda.
            final_agent: Último agente que trabalhou na demanda.
            status:      "success" ou "failed".
            summary:     Resumo do que foi entregue.
        """
        trace = self._get_trace(demand_id)
        trace.update(
            output={"summary": summary, "final_agent": final_agent},
            metadata={
                "final_status": status,
                "completed_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        trace.event(
            name="demand.completed",
            metadata={
                "final_agent": final_agent,
                "status": status,
                "summary": summary,
            },
        )

        self._langfuse.flush()
        self._active_traces.pop(demand_id, None)

    def get_trace(self, demand_id: str) -> Any:
        """Retorna o trace ativo de uma demanda (para criação de spans filhos)."""
        return self._get_trace(demand_id)

    def _get_trace(self, demand_id: str) -> Any:
        trace = self._active_traces.get(demand_id)
        if trace is None:
            raise KeyError(
                f"Nenhum trace ativo para demand_id='{demand_id}'. "
                "Chame DemandTracker.start() antes de registrar eventos."
            )
        return trace
