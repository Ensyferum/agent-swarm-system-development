"""
Marcus — Exemplo de Agente Dev com skills instrumentadas.

Demonstra como um agente técnico usa BaseAgent, @trace_skill,
trace_llm_call e TokenMonitor para rastrear cada etapa de
implementação de uma feature.
"""

import os
import time

os.environ.setdefault("LANGFUSE_PUBLIC_KEY", "pk-lf-...")
os.environ.setdefault("LANGFUSE_SECRET_KEY", "sk-lf-...")
os.environ.setdefault("LANGFUSE_HOST", "http://localhost:3000")

from observability.langfuse.instrumentation import (
    BaseAgent,
    TokenMonitor,
    trace_llm_call,
    trace_skill,
)


# ---------------------------------------------------------------------------
# Skills do Marcus — cada uma decorada com @trace_skill
# ---------------------------------------------------------------------------

@trace_skill(agent_name="marcus", skill_name="analyze_requirement")
def analyze_requirement(trace, demand: dict) -> dict:
    """
    Analisa o requisito e gera um plano de implementação.
    Em produção, chama um LLM para decompor a demanda em tasks.
    """
    # Simular chamada LLM
    time.sleep(0.1)
    prompt_tokens = 450
    completion_tokens = 180

    trace_llm_call(
        trace=trace,
        agent_name="marcus",
        skill_name="analyze_requirement",
        model="gpt-4o",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        input_text=f"Analyze: {demand.get('description', '')}",
        output_text="[Plano de implementação simulado]",
    )

    return {
        "tasks": ["create_schema", "implement_service", "add_tests"],
        "estimated_complexity": "medium",
        "tokens_used": prompt_tokens + completion_tokens,
    }


@trace_skill(agent_name="marcus", skill_name="implement_feature")
def implement_feature(trace, tasks: list, context: dict) -> dict:
    """
    Implementa a feature com base nas tasks do plano.
    Em produção, gera código via LLM.
    """
    time.sleep(0.2)
    prompt_tokens = 1200
    completion_tokens = 800

    trace_llm_call(
        trace=trace,
        agent_name="marcus",
        skill_name="implement_feature",
        model="gpt-4o",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

    return {
        "files_created": ["src/auth/oauth2.py", "src/auth/tests/test_oauth2.py"],
        "files_modified": ["src/main.py"],
        "tokens_used": prompt_tokens + completion_tokens,
    }


@trace_skill(agent_name="marcus", skill_name="create_pr_description")
def create_pr_description(trace, implementation: dict, demand: dict) -> str:
    """Gera a descrição do PR com contexto da implementação."""
    time.sleep(0.05)
    prompt_tokens = 300
    completion_tokens = 150

    trace_llm_call(
        trace=trace,
        agent_name="marcus",
        skill_name="create_pr_description",
        model="gpt-4o-mini",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

    return (
        f"## {demand.get('description', 'Feature implementation')}\n\n"
        f"Arquivos alterados: {implementation.get('files_created', [])}\n"
    )


# ---------------------------------------------------------------------------
# Agente Marcus
# ---------------------------------------------------------------------------

class Marcus(BaseAgent):
    """
    Agente desenvolvedor — implementa features, bugs e refactors.
    Ref: SPEC-V2.md §5 — Marcus
    """

    def __init__(self) -> None:
        super().__init__(name="marcus")
        self.token_monitor = TokenMonitor()

    def execute(self, demand: dict, trace) -> dict:
        """
        Fluxo de implementação:
        1. Analisar requisito
        2. Implementar feature
        3. Gerar descrição do PR
        4. Reportar consumo de tokens
        """
        print(f"[Marcus] Iniciando implementação: {demand['demand_id']}")

        # Etapa 1: Análise
        analysis = analyze_requirement(trace, demand)
        self.token_monitor.record(
            agent="marcus", skill="analyze_requirement",
            model="gpt-4o",
            prompt_tokens=450, completion_tokens=180,
        )

        # Etapa 2: Implementação
        implementation = implement_feature(trace, analysis["tasks"], demand)
        self.token_monitor.record(
            agent="marcus", skill="implement_feature",
            model="gpt-4o",
            prompt_tokens=1200, completion_tokens=800,
        )

        # Etapa 3: PR description
        pr_description = create_pr_description(trace, implementation, demand)
        self.token_monitor.record(
            agent="marcus", skill="create_pr_description",
            model="gpt-4o-mini",
            prompt_tokens=300, completion_tokens=150,
        )

        # Registrar relatório de tokens no trace
        self.token_monitor.flush_to_langfuse(trace, demand["demand_id"])
        report = self.token_monitor.report()

        print(f"[Marcus] Concluído. Tokens totais: {report['total']['total_tokens']}")
        print(f"[Marcus] Custo estimado: USD {report['total']['estimated_cost_usd']}")

        return {
            "status": "completed",
            "pr_ready": True,
            "files": implementation["files_created"] + implementation["files_modified"],
            "pr_description": pr_description,
            "token_report": report["total"],
        }


# ---------------------------------------------------------------------------
# Exemplo de uso
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    marcus = Marcus()

    demanda = {
        "demand_id": "D-2026-001",
        "type": "feature",
        "description": "Adicionar autenticação OAuth2 no serviço de usuários",
        "requester": "product-team",
        "priority": "high",
        "session_id": "sprint-42",
    }

    resultado = marcus.run(demanda)
    print(f"\n✅ Resultado: {resultado}")
    print(f"🔍 Trace: http://localhost:3000/trace/{resultado['_trace_id']}")
