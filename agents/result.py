from typing import Any, Optional
from pydantic import BaseModel, Field

class AgentResult(BaseModel):
    success: bool
    content: str = ""
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def ok(cls, content: str = "", metadata: Optional[dict[str, Any]] = None) -> "AgentResult":
        return cls(
            success=True,
            content=content,
            error=None,
            metadata=metadata or {}
        )

    @classmethod
    def fail(cls, error: str, metadata: Optional[dict[str, Any]] = None) -> "AgentResult":
        return cls(
            success=False,
            content="",
            error=error,
            metadata=metadata or {}
        )
