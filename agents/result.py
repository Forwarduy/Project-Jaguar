from typing import Any, Optional
from pydantic import BaseModel, Field

class AgentResult(BaseModel):
    success: bool
    content: str = ""
    error: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def __str__(self) -> str:
        if self.success:
            return self.content
        return f"❌ {self.error}"

    @classmethod
    def ok(
        cls,
        content: str = "",
        data: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=True,
            content=content,
            error=None,
            data=data,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        error: str,
        data: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=False,
            content="",
            error=error,
            data=data,
            metadata=metadata or {},
        )
