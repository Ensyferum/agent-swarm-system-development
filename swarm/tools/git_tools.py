"""
tools/git_tools.py — Tools de Git para os agentes operarem no workspace.
"""

import os
import subprocess
from pathlib import Path

from langchain_core.tools import tool

WORKSPACE = Path(os.environ.get("SWARM_WORKSPACE", r"C:\Dev\workspace-ia-projects"))


def _run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip() or result.stderr.strip()
    return output if result.returncode == 0 else f"❌ git error: {output}"


@tool
def git_init() -> str:
    """Inicializa um repositório Git no workspace (se ainda não existe)."""
    git_dir = WORKSPACE / ".git"
    if git_dir.exists():
        return "ℹ️  Repositório já inicializado"
    out = _run_git(["init"])
    _run_git(["config", "user.email", "swarm@agent.local"])
    _run_git(["config", "user.name", "Agent Swarm"])
    return f"✅ Git iniciado: {out}"


@tool
def git_status() -> str:
    """Retorna o status atual do repositório Git no workspace."""
    return _run_git(["status", "--short"])


@tool
def git_add_all() -> str:
    """Adiciona todos os arquivos modificados ao stage."""
    return _run_git(["add", "-A"])


@tool
def git_commit(message: str) -> str:
    """
    Faz commit de todos os arquivos staged.

    Args:
        message: Mensagem de commit (formato convencional recomendado)
    """
    _run_git(["add", "-A"])
    return _run_git(["commit", "-m", message])


@tool
def git_create_branch(branch_name: str) -> str:
    """
    Cria e muda para uma nova branch.

    Args:
        branch_name: Nome da branch (ex: 'feat/oauth2-login')
    """
    return _run_git(["checkout", "-b", branch_name])


@tool
def git_log() -> str:
    """Exibe os últimos 5 commits do repositório."""
    return _run_git(["log", "--oneline", "-5"])


GIT_TOOLS = [git_init, git_status, git_add_all, git_commit, git_create_branch, git_log]
