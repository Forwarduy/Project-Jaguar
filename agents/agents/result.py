from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AgentResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    success: bool
    content: str = ""
    error: Optional[str] = None

    @classmethod
    def ok(cls, content: str) -> "AgentResult":
        return cls(success=True, content=content)

    @classmethod
    def fail(cls, error: str) -> "AgentResult":
        return cls(success=False, error=error)

    def __str__(self) -> str:
        return self.content if self.success else f"❌ {self.error}"
