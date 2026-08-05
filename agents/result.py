from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class AgentResult(BaseModel):
    """Standard execution result returned by all agents in Project-Jaguar."""

    success: bool
    content: str = ""
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def __str__(self) -> str:
        if self.success:
            return self.content
        return f"❌ {self.error}"

    @classmethod
    def ok(
        cls,
        content: str,
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=True,
            content=content,
            data=data if data is not None else {},
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        error: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=False,
            error=error,
            metadata=metadata or {},
        )
