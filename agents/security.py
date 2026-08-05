"""Enterprise security, authentication, and credential management for Project Jaguar."""

import os
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar
from pydantic import BaseModel, Field
from config import get_settings


class SecurityContext(BaseModel):
    """Context representing an authenticated enterprise user or service principal."""
    principal_id: str
    roles: List[str] = Field(default_factory=list)
    is_authenticated: bool = True


class CredentialManager:
    """Secure manager for handling sensitive runtime credentials and masking."""

    @staticmethod
    def mask_secret(secret: Optional[str], visible_chars: int = 4) -> str:
        """Mask a sensitive string for safe logging and debugging."""
        if not secret or len(secret) <= visible_chars:
            return "****"
        return "*" * (len(secret) - visible_chars) + secret[-visible_chars:]

    @staticmethod
    def validate_environment_secrets() -> Dict[str, bool]:
        """Validate presence of mandatory enterprise secrets."""
        settings = get_settings()
        return {
            "anthropic_api_key": bool(settings.anthropic_api_key),
        }


F = TypeVar("F", bound=Callable[..., Any])


def requires_auth(required_role: Optional[str] = None) -> Callable[[F], F]:
    """Decorator to enforce authentication and optional role-based access control."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            settings = get_settings()
            token = os.getenv("JAGUAR_AUTH_TOKEN")
            
            # If enforcement is active, validate token
            if getattr(settings, "enforce_auth", False) and not token:
                raise PermissionError("Authentication token missing or invalid.")
            
            if required_role:
                user_roles = [r.strip() for r in os.getenv("JAGUAR_ROLES", "").split(",") if r.strip()]
                if required_role not in user_roles:
                    raise PermissionError(f"Access denied. Required role: {required_role}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
