from __future__ import annotations
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field


class AgentResult(BaseModel):
    """Estructura inmutable estandarizada para la respuesta de cualquier agente."""

    model_config = ConfigDict(frozen=True)

    success: bool
    content: str = ""
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def ok(cls, content: str, metadata: Optional[dict[str, Any]] = None) -> AgentResult:
        """Crea un resultado exitoso con contenido y metadatos opcionales."""
        return cls(success=True, content=content, metadata=metadata or {})

    @classmethod
    def fail(cls, error: str | Exception, metadata: Optional[dict[str, Any]] = None) -> AgentResult:
        """Crea un resultado fallido registrando el mensaje de error o excepción."""
        err_msg = str(error) if isinstance(error, Exception) else str(error)
        return cls(success=False, error=err_msg, metadata=metadata or {})

    def __str__(self) -> str:
        return self.content if self.success else f"❌ {self.error}"
