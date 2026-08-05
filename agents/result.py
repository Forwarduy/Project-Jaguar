"""Result container for agent execution outputs."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """Encapsulates the outcome, data, and metadata of an agent execution."""

    success: bool = True
    content: str = ""
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

    def __str__(self) -> str:
        """Returns string representation to match test suite expectations."""
        if self.success:
            return self.content
        return f"❌ {self.content}"

    @classmethod
    def ok(
        cls,
        content: str = "",
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        """Factory method for successful results."""
        return cls(
            success=True,
            content=content,
            data=data or {},
            metadata=metadata or {},
            error=None,
        )

    @classmethod
    def fail(
        cls,
        content: str = "",
        error: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        """Factory method for failed results."""
        return cls(
            success=False,
            content=content,
            error=error if error is not None else content,
            data=data or {},
            metadata=metadata or {},
        )
