"""
tools/filesystem.py — Tools de leitura e escrita de arquivos no workspace.

Cada tool é uma função decorada com @tool do LangChain,
para que os agentes possam invocá-las diretamente.
"""

import os
import shutil
from pathlib import Path

from langchain_core.tools import tool

WORKSPACE = Path(os.environ.get("SWARM_WORKSPACE", r"C:\Dev\workspace-ia-projects"))


def _safe_path(relative_path: str) -> Path:
    """Garante que o path está dentro do workspace (evita path traversal)."""
    target = (WORKSPACE / relative_path).resolve()
    if not str(target).startswith(str(WORKSPACE.resolve())):
        raise ValueError(f"Path fora do workspace: {relative_path}")
    return target


@tool
def write_file(relative_path: str, content: str) -> str:
    """
    Escreve (ou sobrescreve) um arquivo no workspace do projeto.

    Args:
        relative_path: Caminho relativo ao workspace (ex: 'src/auth/oauth2.py')
        content: Conteúdo completo do arquivo
    """
    target = _safe_path(relative_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"✅ Arquivo criado: {relative_path} ({len(content)} chars)"


@tool
def read_file(relative_path: str) -> str:
    """
    Lê o conteúdo de um arquivo do workspace.

    Args:
        relative_path: Caminho relativo ao workspace
    """
    target = _safe_path(relative_path)
    if not target.exists():
        return f"❌ Arquivo não encontrado: {relative_path}"
    return target.read_text(encoding="utf-8")


@tool
def list_files(directory: str = "") -> str:
    """
    Lista os arquivos em um diretório do workspace.

    Args:
        directory: Diretório relativo ao workspace (vazio = raiz)
    """
    target = _safe_path(directory) if directory else WORKSPACE
    if not target.exists():
        return f"❌ Diretório não encontrado: {directory}"
    files = sorted(target.rglob("*"))
    lines = [str(f.relative_to(WORKSPACE)) for f in files if f.is_file()]
    return "\n".join(lines) if lines else "(vazio)"


@tool
def create_directory(relative_path: str) -> str:
    """
    Cria um diretório no workspace.

    Args:
        relative_path: Caminho relativo ao workspace
    """
    target = _safe_path(relative_path)
    target.mkdir(parents=True, exist_ok=True)
    return f"✅ Diretório criado: {relative_path}"


FILESYSTEM_TOOLS = [write_file, read_file, list_files, create_directory]
