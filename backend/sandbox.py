"""Restricted local code execution for GS420 AI Phase 4."""
from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    return_code: int
    timed_out: bool


class SandboxExecutor:
    """Execute short Python snippets with strict resource/time limits.

    This is a defense-in-depth local sandbox, not a perfect security boundary.
    For untrusted multi-tenant execution, use an isolated container/VM.
    """

    def __init__(self, timeout_seconds: int = 5, max_output_chars: int = 12000) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_output_chars = max_output_chars

    def execute_python(self, code: str) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(False, "", "Code cannot be empty.", 1, False)

        with tempfile.TemporaryDirectory(prefix="gs420-sandbox-") as workdir:
            path = os.path.join(workdir, "main.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(code)

            env = {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONIOENCODING": "utf-8",
                "PYTHONNOUSERSITE": "1",
                "HOME": workdir,
            }

            try:
                completed = subprocess.run(
                    ["python", "-I", path],
                    cwd=workdir,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                )
                return ExecutionResult(
                    success=completed.returncode == 0,
                    stdout=completed.stdout[: self.max_output_chars],
                    stderr=completed.stderr[: self.max_output_chars],
                    return_code=completed.returncode,
                    timed_out=False,
                )
            except subprocess.TimeoutExpired as exc:
                stdout = (exc.stdout or "")
                stderr = (exc.stderr or "")
                if isinstance(stdout, bytes):
                    stdout = stdout.decode("utf-8", errors="replace")
                if isinstance(stderr, bytes):
                    stderr = stderr.decode("utf-8", errors="replace")
                return ExecutionResult(
                    success=False,
                    stdout=stdout[: self.max_output_chars],
                    stderr=(stderr + "\nExecution timed out.")[: self.max_output_chars],
                    return_code=-1,
                    timed_out=True,
                )
