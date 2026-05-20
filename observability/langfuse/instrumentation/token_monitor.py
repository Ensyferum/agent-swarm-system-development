"""
token_monitor — Monitor de consumo de tokens por agente e skill.

Agrega métricas de tokens de todas as chamadas LLM e permite
consultar o consumo acumulado por agente, skill ou demanda.

Uso:
    from observability.langfuse.instrumentation.token_monitor import TokenMonitor

    monitor = TokenMonitor()
    monitor.record(agent="marcus", skill="create_component",
                   model="gpt-4o", prompt_tokens=500, completion_tokens=200)

    report = monitor.report()
    monitor.flush_to_langfuse(trace, demand_id="D-001")
"""

from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from langfuse import Langfuse


# Custo aproximado por 1M tokens (USD) — atualize conforme pricing atual
MODEL_COST_PER_1M: dict[str, dict[str, float]] = {
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4-turbo": {"prompt": 10.00, "completion": 30.00},
    "claude-3-5-sonnet": {"prompt": 3.00, "completion": 15.00},
    "claude-3-haiku": {"prompt": 0.25, "completion": 1.25},
    "llama-3-70b": {"prompt": 0.00, "completion": 0.00},
}


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    calls: int = 0
    models: list[str] = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def estimated_cost_usd(self) -> float:
        total = 0.0
        for model in set(self.models):
            pricing = MODEL_COST_PER_1M.get(model, {"prompt": 0.0, "completion": 0.0})
            total += (self.prompt_tokens / 1_000_000) * pricing["prompt"]
            total += (self.completion_tokens / 1_000_000) * pricing["completion"]
        return round(total, 6)


class TokenMonitor:
    """
    Agrega e reporta consumo de tokens por agente e skill.

    Thread-safe para uso em ambientes de agente único (sem concorrência).
    Para múltiplos agentes paralelos, use uma instância por agente.
    """

    def __init__(self) -> None:
        self._langfuse = Langfuse(
            public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
            secret_key=os.environ["LANGFUSE_SECRET_KEY"],
            host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000"),
        )
        # {agent_name: TokenUsage}
        self._by_agent: dict[str, TokenUsage] = defaultdict(TokenUsage)
        # {agent_name.skill_name: TokenUsage}
        self._by_skill: dict[str, TokenUsage] = defaultdict(TokenUsage)

    def record(
        self,
        agent: str,
        skill: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        """
        Registra o uso de tokens de uma chamada LLM.

        Args:
            agent:             Codinome do agente (ex: "marcus").
            skill:             Nome da skill (ex: "create_component").
            model:             Modelo usado (ex: "gpt-4o").
            prompt_tokens:     Tokens do prompt.
            completion_tokens: Tokens da resposta.
        """
        key = f"{agent}.{skill}"

        for usage in (self._by_agent[agent], self._by_skill[key]):
            usage.prompt_tokens += prompt_tokens
            usage.completion_tokens += completion_tokens
            usage.calls += 1
            usage.models.append(model)

    def report(self) -> dict[str, Any]:
        """
        Retorna um relatório agregado de consumo de tokens.

        Returns:
            Dicionário com consumo por agente e por skill.
        """
        total = TokenUsage()
        for usage in self._by_agent.values():
            total.prompt_tokens += usage.prompt_tokens
            total.completion_tokens += usage.completion_tokens
            total.calls += usage.calls

        return {
            "total": {
                "prompt_tokens": total.prompt_tokens,
                "completion_tokens": total.completion_tokens,
                "total_tokens": total.total_tokens,
                "calls": total.calls,
                "estimated_cost_usd": total.estimated_cost_usd(),
            },
            "by_agent": {
                agent: {
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "total_tokens": u.total_tokens,
                    "calls": u.calls,
                    "estimated_cost_usd": u.estimated_cost_usd(),
                }
                for agent, u in self._by_agent.items()
            },
            "by_skill": {
                skill: {
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "total_tokens": u.total_tokens,
                    "calls": u.calls,
                }
                for skill, u in self._by_skill.items()
            },
        }

    def flush_to_langfuse(self, trace: Any, demand_id: str) -> None:
        """
        Registra o relatório de tokens como evento no trace LangFuse.

        Args:
            trace:     Objeto LangFuse Trace da demanda.
            demand_id: ID da demanda (para metadados).
        """
        report = self.report()
        trace.event(
            name="token_usage.summary",
            metadata={"demand_id": demand_id, **report},
        )
        self._langfuse.flush()

    def reset(self) -> None:
        """Limpa os contadores para reutilização do monitor."""
        self._by_agent.clear()
        self._by_skill.clear()
