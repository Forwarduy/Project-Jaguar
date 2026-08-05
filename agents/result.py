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
