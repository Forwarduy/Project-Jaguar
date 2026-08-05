"""Data contracts for agent execution results."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class AgentResult(BaseModel):
    """Standard result structure returned by all Project-Jaguar agents."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    content: str
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        content: str,
        data: Optional[Any] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        """Factory method to construct a successful AgentResult."""
        return cls(
            success=True,
            content=content,
            data=data,
            error=None,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        error: str,
        content: str = "",
        data: Optional[Any] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        """Factory method to construct a failed AgentResult."""
        return cls(
            success=False,
            content=content or error,
            data=data,
            error=error,
            metadata=metadata or {},
        )
