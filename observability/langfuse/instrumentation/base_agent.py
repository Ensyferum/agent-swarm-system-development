"""
BaseAgent — Classe base para todos os agentes do swarm.

Todos os agentes herdam desta classe para obter tracing automático
via LangFuse sem repetir código de instrumentação.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from typing import Any

from langfuse import Langfuse
from langfuse.decorators import langfuse_context


class BaseAgent(ABC):
    """
    Classe base com tracing LangFuse integrado.

    Cada agente concreto deve:
    1. Herdar de BaseAgent
    2. Definir self.name com seu codinome (ex: "massuia", "marcus")
    3. Implementar o método execute()

    O tracing é iniciado automaticamente em run() e encerrado
    ao final da execução ou em caso de erro.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._langfuse = Langfuse(
            public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
            secret_key=os.environ["LANGFUSE_SECRET_KEY"],
            host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000"),
        )

    def run(self, demand: dict[str, Any]) -> dict[str, Any]:
        """
        Executa o agente com tracing automático.

        Args:
            demand: Dicionário com os dados da demanda.
                    Deve conter ao menos: demand_id, type, description

        Returns:
            Dicionário com resultado da execução e metadados de trace.
        """
        demand_id = demand.get("demand_id", "unknown")
        demand_type = demand.get("type", "unknown")

        trace = self._langfuse.trace(
            id=demand_id,
            name=f"{self.name}.run",
            user_id=demand.get("requester"),
            session_id=demand.get("session_id", demand_id),
            metadata={
                "agent": self.name,
                "demand_type": demand_type,
                "source": demand.get("source", "swarm"),
            },
            tags=[self.name, demand_type],
        )

        span = trace.span(
            name=f"{self.name}.execute",
            input={"demand_id": demand_id, "type": demand_type},
            metadata={"agent": self.name},
        )

        start_time = time.time()
        try:
            result = self.execute(demand, trace)
            elapsed = time.time() - start_time

            span.end(
                output=result,
                metadata={"duration_seconds": round(elapsed, 3), "status": "success"},
            )
            trace.update(metadata={"final_status": "success", "agent": self.name})

            return {**result, "_trace_id": trace.id, "_agent": self.name}

        except Exception as exc:
            elapsed = time.time() - start_time
            span.end(
                metadata={
                    "duration_seconds": round(elapsed, 3),
                    "status": "error",
                    "error": str(exc),
                }
            )
            trace.update(
                metadata={"final_status": "error", "error": str(exc), "agent": self.name}
            )
            raise

        finally:
            self._langfuse.flush()

    @abstractmethod
    def execute(self, demand: dict[str, Any], trace: Any) -> dict[str, Any]:
        """
        Lógica principal do agente. Implementado por cada subclasse.

        Args:
            demand: Dados da demanda.
            trace:  Objeto LangFuse Trace — passe para skills que fazem
                    chamadas LLM para criar spans filhos.

        Returns:
            Dicionário com o resultado da execução.
        """
        ...

    def log_event(self, trace: Any, name: str, data: dict[str, Any]) -> None:
        """Registra um evento pontual dentro de um trace existente."""
        trace.event(name=name, metadata={"agent": self.name, **data})
