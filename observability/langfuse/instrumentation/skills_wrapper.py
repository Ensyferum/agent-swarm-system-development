"""
skills_wrapper — Decorator @trace_skill para instrumentar skills dos agentes.

Uso:
    from observability.langfuse.instrumentation.skills_wrapper import trace_skill

    @trace_skill(agent_name="marcus", skill_name="create_component")
    def create_component(trace, demand, **kwargs):
        ...
"""

from __future__ import annotations

import functools
import time
from typing import Any, Callable


def trace_skill(agent_name: str, skill_name: str):
    """
    Decorator que envolve uma skill com um LangFuse span.

    O primeiro argumento da função decorada DEVE ser o objeto `trace`
    recebido de BaseAgent.execute().

    Args:
        agent_name: Codinome do agente (ex: "marcus").
        skill_name: Nome da skill (ex: "create_component").
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(trace: Any, *args, **kwargs) -> Any:
            span_name = f"{agent_name}.{skill_name}"

            span = trace.span(
                name=span_name,
                input={"args_count": len(args), "kwargs_keys": list(kwargs.keys())},
                metadata={"agent": agent_name, "skill": skill_name},
            )

            start_time = time.time()
            try:
                result = func(trace, *args, **kwargs)
                elapsed = time.time() - start_time

                span.end(
                    output=_safe_output(result),
                    metadata={
                        "duration_seconds": round(elapsed, 3),
                        "status": "success",
                    },
                )
                return result

            except Exception as exc:
                elapsed = time.time() - start_time
                span.end(
                    metadata={
                        "duration_seconds": round(elapsed, 3),
                        "status": "error",
                        "error": str(exc),
                    }
                )
                raise

        return wrapper

    return decorator


def trace_llm_call(
    trace: Any,
    agent_name: str,
    skill_name: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    input_text: str = "",
    output_text: str = "",
) -> None:
    """
    Registra uma chamada LLM com métricas de token dentro de um trace.

    Use esta função após cada chamada ao modelo dentro de uma skill.

    Args:
        trace:             Objeto LangFuse Trace.
        agent_name:        Codinome do agente.
        skill_name:        Nome da skill que fez a chamada.
        model:             Nome do modelo (ex: "gpt-4o", "claude-3-5-sonnet").
        prompt_tokens:     Tokens usados no prompt.
        completion_tokens: Tokens gerados na resposta.
        input_text:        Texto enviado ao modelo (opcional, para debug).
        output_text:       Texto recebido do modelo (opcional, para debug).
    """
    total_tokens = prompt_tokens + completion_tokens

    trace.generation(
        name=f"{agent_name}.{skill_name}.llm",
        model=model,
        input=input_text or "[omitted]",
        output=output_text or "[omitted]",
        usage={
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
        metadata={"agent": agent_name, "skill": skill_name},
    )


def _safe_output(result: Any) -> Any:
    """Trunca outputs muito grandes para não sobrecarregar o LangFuse."""
    if isinstance(result, str) and len(result) > 2000:
        return result[:2000] + "... [truncated]"
    if isinstance(result, dict):
        return {k: _safe_output(v) for k, v in result.items()}
    return result
