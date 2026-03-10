from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable, Tuple

REPO_ROOT = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> Tuple[bool, str]:
    try:
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        ok = result.returncode == 0
        out = (result.stdout or "") + (result.stderr or "")
        return ok, out.strip()
    except Exception as exc:
        return False, str(exc)


def _set_remote_with_token() -> Tuple[bool, str]:
    token = os.getenv("GIT_TOKEN", "")
    user = os.getenv("GIT_USERNAME", "")
    repo = os.getenv("GIT_REPO", "")

    if not (token and user and repo):
        return True, ""

    url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
    ok, out = _run(["git", "remote", "set-url", "origin", url])
    if not ok:
        return False, f"Falha ao configurar remote com token: {out}"
    return True, ""


def commit_and_push(paths: Iterable[str], message: str) -> Tuple[bool, str]:
    paths = list(paths)
    branch = os.getenv("GIT_BRANCH", "main")

    ok, out = _set_remote_with_token()
    if not ok:
        return False, out

    ok, out = _run(["git", "add", *paths])
    if not ok:
        return False, f"git add falhou: {out}"

    ok, out = _run(["git", "commit", "-m", message])
    if not ok:
        if "nothing to commit" in out.lower():
            return True, "Nada para commit."
        return False, f"git commit falhou: {out}"

    ok, out = _run(["git", "push", "origin", branch])
    if not ok:
        return False, f"git push falhou: {out}"

    return True, "Pedido enviado para o GitHub."
