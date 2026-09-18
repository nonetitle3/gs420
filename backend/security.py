"""Phase 12 security helpers."""
from __future__ import annotations

import os
import secrets


def generate_secret(length: int = 32) -> str:
    if length < 16:
        raise ValueError("Secret length must be at least 16.")
    return secrets.token_urlsafe(length)


def redacted_environment() -> dict[str, str]:
    sensitive = ("TOKEN", "SECRET", "PASSWORD", "KEY")
    return {k: ("***" if any(x in k.upper() for x in sensitive) else v)
            for k, v in os.environ.items() if k.startswith("GS420_")}
