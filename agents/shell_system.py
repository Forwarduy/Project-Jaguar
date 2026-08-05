"""System environment verification and diagnostic guardrails."""

import os
import sys
from typing import List, Tuple

REQUIRED_PYTHON_VERSION: Tuple[int, int] = (3, 10)
CRITICAL_ENV_VARS: List[str] = ["ANTHROPIC_API_KEY"]


class SystemValidationError(Exception):
    """Raised when critical environment or system runtime checks fail."""

    pass


def verify_runtime_environment() -> None:
    """Validate system requirements prior to core agent execution.

    Raises:
        SystemValidationError: If Python version is incompatible or required
            environment parameters are missing.
    """
    if sys.version_info < REQUIRED_PYTHON_VERSION:
        raise SystemValidationError(
            f"Project-Jaguar requires Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}+. "
            f"Current version: {sys.version.split()[0]}"
        )

    missing_vars = [var for var in CRITICAL_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        raise SystemValidationError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please verify your .env configuration."
        )


def get_system_health() -> dict:
    """Return runtime system context for telemetry and logging."""
    return {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "anthropic_key_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "active_env": os.getenv("ENVIRONMENT", "development"),
    }
